from dataclasses import dataclass
from typing import Type
from matplotlib import pyplot as plt

import numpy as np
from arm_lib import LINEAR_ELEMENT_COLOR, Degrees
from arm_lib.arm_lib import print_matrix
from arm_lib.frame import Frame2D
from arm_lib.joint import Joint
from arm_lib.plotter import Plotter


@dataclass
class LinearElement(Joint):
    length: float
    angle_offset: Degrees
    layer: int

    def transform(self, frame: Frame2D):
        orientation = frame.orientation + self.angle_offset
        naive_offset = np.matrix([[self.length], [0.0]])
        rad = np.radians(orientation)
        cos = np.cos(rad)
        sin = np.sin(rad)
        rotation = np.matrix([[cos, -sin], [sin, cos]])
        translation = np.matrix([[frame.origin[0]], [frame.origin[1]]])
        result = rotation * naive_offset + translation
        result = np.squeeze(result.tolist())
        return Frame2D((result[0], result[1]), orientation)

    def plotter(self, ax: plt.Axes, frame: Frame2D) -> Type[Plotter]:
        return LinearElementPlot(ax, frame, self)

    def print_transform(self) -> str:
        elements = [
            [
                f"cos({self.angle_offset:5.3f})",
                f"-sin({self.angle_offset:5.3f})",
                f"{self.length:5.3f}",
            ],
            [
                f"sin({self.angle_offset:5.3f})",
                f"cos({self.angle_offset:5.3f})",
                f"{0:5.3f}",
            ],
            [f"{0:5.3f}", f"{0:5.3f}", f"{1:5.3f}"],
        ]

        return print_matrix(elements)


class LinearElementPlot(Plotter):
    def __init__(self, ax: plt.Axes, frame: Frame2D, joint: LinearElement):
        self.joint = joint

        resulting_frame = self.joint.transform(frame)

        self.line = plt.Line2D(
            [frame.origin[0], resulting_frame.origin[0]],
            [frame.origin[1], resulting_frame.origin[1]],
            marker="o",
            color=LINEAR_ELEMENT_COLOR[self.joint.layer % len(LINEAR_ELEMENT_COLOR)],
        )

        ax.add_line(self.line)

    def update(self, frame: Frame2D):
        resulting_frame = self.joint.transform(frame)
        self.line.set_data(
            [frame.origin[0], resulting_frame.origin[0]],
            [frame.origin[1], resulting_frame.origin[1]],
        )
