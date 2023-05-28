from dataclasses import dataclass
from typing import List, Type, Union

from matplotlib import pyplot as plt
import matplotlib.patches as pat
from arm_lib import (
    REVOLUTE_FULFILLED_COLOR,
    REVOLUTE_FULFILLED_ERROR,
    REVOLUTE_POTENTIAL_COLOR,
    REVOLUTE_RADIUS,
    Degrees,
)
from arm_lib.arm_lib import print_matrix
from arm_lib.frame import Frame2D
from arm_lib.joint import Joint, JointLimitError
from arm_lib.plotter import Plotter


@dataclass
class LimitedRevoluteJoint(Joint):
    min: Degrees
    max: Degrees
    rotation: Degrees
    layers: List[int]

    def rotate(self, angle: Degrees) -> Union[Degrees, JointLimitError]:
        if angle < self.min:
            raise JointLimitError(
                f"input angle {angle:.2f} less than minimum: {self.min:.2f}"
            )
        elif angle > self.max:
            raise JointLimitError(
                f"input angle {angle:.2f} greater than maximum: {self.max:.2f}"
            )
        else:
            self.rotation = angle

    def transform(self, frame: Frame2D):
        return Frame2D(frame.origin, frame.orientation + self.rotation)

    def plotter(self, ax: plt.Axes, frame: Frame2D) -> Type[Plotter]:
        return LimitedRevolutePlot(ax, frame, self)

    def print_transform(self) -> str:
        elements = [
            [
                f"cos({self.rotation:5.3f})",
                f"-sin({self.rotation:5.3f})",
                f"{0:5.3f}",
            ],
            [
                f"sin({self.rotation:5.3f})",
                f"cos({self.rotation:5.3f})",
                f"{0:5.3f}",
            ],
            [f"{0:5.3f}", f"{0:5.3f}", f"{1:5.3f}"],
        ]

        return print_matrix(elements)


class LimitedRevolutePlot(Plotter):
    def __init__(self, ax: plt.Axes, frame: Frame2D, joint: LimitedRevoluteJoint):
        self.joint = joint

        self.potential_arc = pat.Wedge(
            frame.origin,
            REVOLUTE_RADIUS,
            self.joint.rotation + frame.orientation,
            self.joint.max + frame.orientation,
            color=REVOLUTE_POTENTIAL_COLOR,
        )

        self.fulfilled_arc = pat.Wedge(
            frame.origin,
            REVOLUTE_RADIUS,
            self.joint.min + frame.orientation,
            self.joint.rotation + frame.orientation,
            color=REVOLUTE_FULFILLED_COLOR,
        )

        ax.add_patch(self.potential_arc)
        ax.add_patch(self.fulfilled_arc)

    def update(self, frame: Frame2D):
        self.potential_arc.set_center(frame.origin)
        self.fulfilled_arc.set_center(frame.origin)

        self.potential_arc.set_theta1(self.joint.rotation + frame.orientation)
        self.potential_arc.set_theta2(self.joint.max + frame.orientation)

        self.fulfilled_arc.set_theta1(self.joint.min + frame.orientation)
        self.fulfilled_arc.set_theta2(self.joint.rotation + frame.orientation)

    def error(self):
        self.fulfilled_arc.set_color(REVOLUTE_FULFILLED_ERROR)

    def recover(self):
        self.fulfilled_arc.set_color(REVOLUTE_FULFILLED_COLOR)
