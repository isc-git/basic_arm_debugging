from dataclasses import dataclass
from typing import Type, Union

from matplotlib import pyplot as plt
import matplotlib.patches as pat
from arm_lib import REVOLUTE_FULFILLED_COLOR, REVOLUTE_FULFILLED_ERROR, REVOLUTE_POTENTIAL_COLOR, REVOLUTE_RADIUS

from arm_lib.arm_lib import Degrees, Frame2D, Joint, JointLimitError, Plotter


@dataclass
class LimitedRevoluteJoint(Joint):
    min: Degrees
    max: Degrees
    rotation: Degrees

    def rotate(self, angle: Degrees) -> Union[Degrees, JointLimitError]:
        if angle < self.min:
            raise JointLimitError(f"input angle {angle:.2f} less than minimum: {self.min:.2f}")
        elif angle > self.max:
            raise JointLimitError(f"input angle {angle:.2f} greater than maximum: {self.max:.2f}")
        else:
            self.rotation = angle
    
    def transform(self, frame: Frame2D):
        return Frame2D(frame.origin, frame.orientation + self.rotation)

    def plotter(self, ax: plt.Axes, frame: Frame2D) -> Type[Plotter]:
        return LimitedRevolutePlot(ax, frame, self)

class LimitedRevolutePlot(Plotter):
    def __init__(
        self,
        ax: plt.Axes,
        frame: Frame2D,
        joint: LimitedRevoluteJoint
    ):
        self.joint = joint

        self.potential_arc = pat.Wedge(
            frame.origin,
            REVOLUTE_RADIUS,
            self.joint.rotation + frame.orientation,
            self.joint.max + frame.orientation,
            color = REVOLUTE_POTENTIAL_COLOR
        )

        self.fulfilled_arc = pat.Wedge(
            frame.origin,
            REVOLUTE_RADIUS,
            self.joint.min + frame.orientation,
            self.joint.rotation + frame.orientation,
            color = REVOLUTE_FULFILLED_COLOR
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