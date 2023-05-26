import matplotlib.pyplot as plt

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Type

Degrees = float

class ArmState(Enum):
    OK = 0
    ERROR = 1

@dataclass
class Frame2D:
    origin: Tuple[float, float]
    orientation: Degrees

@dataclass
class Plotter:
    def update(self, frame: Frame2D):
        raise NotImplementedError

    def error(self):
        raise NotImplementedError

    def recover(self):
        raise NotImplementedError

@dataclass
class Joint:
    def transform(self, frame: Frame2D):
        raise NotImplementedError
    
    def plotter(self, ax: plt.Axes, frame: Frame2D) -> Type[Plotter]:
        raise NotImplementedError

class JointLimitError(Exception):
    pass