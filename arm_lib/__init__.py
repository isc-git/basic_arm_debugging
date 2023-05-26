REVOLUTE_RADIUS: float = 0.2
REVOLUTE_COMPLETE_COLOR: str = "#fceb88"
REVOLUTE_POTENTIAL_COLOR: str = "#e6f2ec"
REVOLUTE_FULFILLED_COLOR: str = "#b3ffd5"
REVOLUTE_FULFILLED_ERROR: str = "red"
LINEAR_ELEMENT_COLOR: str = [
    "#fab1ea",
    "#a77aff",
    "#7affbf",
    "#fae170"
]    

from .arm_lib import *
from .arm import *
from .limited_revolute_joint import *
from .linear_element import *
from .revolute_joint import *