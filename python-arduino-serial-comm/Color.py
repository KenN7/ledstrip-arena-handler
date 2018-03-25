from enum import Enum


class Color(Enum):
    NONE = "0,0,0"
    RED = "255,0,0"
    GREEN = "0,255,0"
    BLUE = "0,0,255"
    YELLOW = "255,255,0"
    WHITE = "255,255,255"
    OMIT = "-1,-1,-1"
