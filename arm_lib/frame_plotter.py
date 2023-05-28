from matplotlib import pyplot as plt
from matplotlib import patches as patch

from arm_lib import FRAME_2D_LENGTH
from arm_lib.frame import Frame2D
from arm_lib.linear_element import LinearElement
from arm_lib.plotter import Plotter


class Frame2DPlotter(Plotter):
    def __init__(self, ax: plt.Axes, frame: Frame2D):
        self.x_pseudo_joint = LinearElement(FRAME_2D_LENGTH, 0.0, None)
        self.y_pseudo_joint = LinearElement(FRAME_2D_LENGTH, 90.0, None)

        x_frame = self.x_pseudo_joint.transform(frame)
        y_frame = self.y_pseudo_joint.transform(frame)

        x_frame_delta = frame.position_delta(x_frame)
        y_frame_delta = frame.position_delta(y_frame)

        x, y = frame.origin

        self.x_arrow = patch.FancyArrow(
            x,
            y,
            x_frame_delta[0],
            x_frame_delta[1],
            color="blue",
            head_width=0.1 * FRAME_2D_LENGTH,
        )

        self.y_arrow = patch.FancyArrow(
            x,
            y,
            y_frame_delta[0],
            y_frame_delta[1],
            color="red",
            head_width=0.1 * FRAME_2D_LENGTH,
        )

        ax.add_patch(self.x_arrow)
        ax.add_patch(self.y_arrow)

    def update(self, frame: Frame2D):
        x_frame = self.x_pseudo_joint.transform(frame)
        y_frame = self.y_pseudo_joint.transform(frame)

        x_frame_delta = frame.position_delta(x_frame)
        y_frame_delta = frame.position_delta(y_frame)

        x, y = frame.origin

        self.x_arrow.set_data(
            x,
            y,
            x_frame_delta[0],
            x_frame_delta[1],
        )

        self.y_arrow.set_data(
            x,
            y,
            y_frame_delta[0],
            y_frame_delta[1],
        )
