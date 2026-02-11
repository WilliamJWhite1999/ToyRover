"""
This module contains various command types used within the simulator.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal

import numpy as np

Vec2 = np.ndarray[tuple[Literal[2]], np.dtype[np.float64]]
""" Type definition for a numpy array of shape (2,) """


class Command(StrEnum):
    """
    An Enum defining the set of valid commands for use in the Simulator. Each command contains
    implicit documentation.
    """

    doc: str
    """ Documentation attached to each enum field. """

    def __new__(cls, value: str, doc: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.doc = doc
        return obj

    FILE = (
        "FILE",
        "Read commands from the provided filepath. Accepts one arg in the form of a filepath. ",
    )
    PLACE = (
        "PLACE",
        "Place the rover at the specified x,y coordinates with given direction. Accepts one arg in "
        "the form x,y,Direction e.g. 1,3,NORTH",
    )
    MOVE = ("MOVE", "Move the rover one place forwards. ")
    LEFT = ("LEFT", "Rotate the rover 90 degrees to the left. ")
    RIGHT = ("RIGHT", "Rotate the rover 90 degrees to the right. ")
    REPORT = ("REPORT", "Display the current location of the rover. ")
    HELP = ("HELP", "Display a help message. ")
    EXIT = ("EXIT", "Exit the simulator. ")


class Direction(StrEnum):
    """
    This enum contains a set of pre-defined cardinal directions. Each direction can be converted
    to a Vec2 type using the as_vec2 function.
    """

    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

    def as_vec2(self) -> Vec2:
        """
        Return the Direction enum as a Vec2.
        """
        match self:
            case Direction.NORTH:
                return np.array([0, 1], dtype=np.float64)
            case Direction.EAST:
                return np.array([1, 0], dtype=np.float64)
            case Direction.SOUTH:
                return np.array([0, -1], dtype=np.float64)
            case Direction.WEST:
                return np.array([-1, 0], dtype=np.float64)


@dataclass
class PlaceArgs:
    """
    Container for arguments read in for a Place command operation.
    """

    position: Vec2 = field()
    """ Vec2 position vector """

    direction: Vec2 = field()
    """ Vec2 direction vector """
