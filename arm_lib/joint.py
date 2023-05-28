from dataclasses import dataclass
from typing import Type

from matplotlib import pyplot as plt
from arm_lib.frame import Frame2D
from arm_lib.plotter import Plotter


@dataclass
class Joint:
    def transform(self, frame: Frame2D):
        raise NotImplementedError

    def plotter(self, ax: plt.Axes, frame: Frame2D) -> Type[Plotter]:
        raise NotImplementedError

    def print_transform(self) -> str:
        raise NotImplementedError


class JointLimitError(Exception):
    pass
