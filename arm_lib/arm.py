from typing import List, Type
from matplotlib import pyplot as plt

from pyparsing import Optional

from arm_lib.arm_lib import Frame2D, Joint, Plotter


class Arm:
    def __init__(
        self,
        joint_vector: List[Type[Joint]],
        global_frame: Frame2D
    ):
        self.arm = joint_vector
        self.base_frame = global_frame
        self.plot: Optional[List[Type[Plotter]]] = None
    
    def initialize_plotters(self, ax: plt.Axes):
        assert self.plot == None, "already initialized"
        plotters = []

        frame = self.base_frame
        for joint in self.arm:
            plotters.append(joint.plotter(ax, frame))
            frame = joint.transform(frame)
        
        self.plot = plotters
    
    def update_plotters(self):
        assert self.plot is not None, "plotters not initialised"

        frame = self.base_frame
        for index, plotter in enumerate(self.plot):
            plotter.update(frame)
            frame = self.arm[index].transform(frame)