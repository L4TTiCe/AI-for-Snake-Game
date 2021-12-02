from enum import Enum


# https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
class Actions(Enum):
    UP = 2
    DOWN = 8
    LEFT = 4
    RIGHT = 6
    NONE = 5
