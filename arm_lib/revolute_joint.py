from dataclasses import dataclass
from typing import List, Type

from matplotlib import pyplot as plt
import matplotlib.patches as pat
import matplotlib.pyplot as plt
from arm_lib import REVOLUTE_COMPLETE_COLOR, REVOLUTE_FULFILLED_ERROR, REVOLUTE_RADIUS

from arm_lib.arm_lib import Degrees, Frame2D, Joint, Plotter

@dataclass
class RevoluteJoint(Joint):
    rotation: Degrees
    layers: List[int]

    def rotate(self, angle: Degrees):
        self.rotation = angle
    
    def transform(self, frame: Frame2D):
        return Frame2D(frame.origin, frame.orientation + self.rotation)
    
    def plotter(self, ax: plt.Axes, frame: Frame2D) -> Type[Plotter]:
        return RevolutePlot(ax, frame, self)
    

class RevolutePlot(Plotter):
    def __init__(
        self,
        ax: plt.Axes,
        frame: Frame2D,
        joint: RevoluteJoint,
    ):
        self.joint = joint

        self.arc = pat.Circle(
            frame.origin,
            REVOLUTE_RADIUS,
            color=REVOLUTE_COMPLETE_COLOR
        )

        ax.add_patch(self.arc)
    
    def update(self, frame: Frame2D):
        self.arc.set_center(frame.origin)

    def error(self):
        self.fulfilled_arc.set_color(REVOLUTE_FULFILLED_ERROR)

    def recover(self):
        self.fulfilled_arc.set_color(REVOLUTE_COMPLETE_COLOR)
