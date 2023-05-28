from dataclasses import dataclass
from typing import Tuple
from typing_extensions import Self

from arm_lib import Degrees


@dataclass
class Frame2D:
    origin: Tuple[float, float]
    orientation: Degrees

    def position_delta(self, rhs: Self) -> Tuple[float, float]:
        delta_x = rhs.origin[0] - self.origin[0]
        delta_y = rhs.origin[1] - self.origin[1]
        return (delta_x, delta_y)
