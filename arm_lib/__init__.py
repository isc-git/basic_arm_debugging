REVOLUTE_RADIUS: float = 0.2
REVOLUTE_POTENTIAL_COLOR: str = "gray"
REVOLUTE_FULFILLED_COLOR: str = "green"
REVOLUTE_FULFILLED_ERROR: str = "red"
LINEAR_ELEMENT_COLOR: str = "black"

from .arm_lib import *
from .arm import *
from .limited_revolute_joint import *
from .linear_element import *