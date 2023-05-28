from dataclasses import dataclass

from arm_lib.frame import Frame2D


@dataclass
class Plotter:
    def update(self, frame: Frame2D):
        raise NotImplementedError

    def error(self):
        raise NotImplementedError

    def recover(self):
        raise NotImplementedError
