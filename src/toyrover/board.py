"""
This module contains the Board that defines the simulation space.
"""

from toyrover.types import Vec2


class Board:
    """
    Board defines the simulation space bounds.
    """

    _x_size: float
    """ Maximum size of the space along the x axis. """

    _y_size: float
    """ Maximum size of the space along the y axis """

    def __init__(self, x_size: float, y_size: float):
        """Initialise the board with a define x and y bound."""
        self._x_size = x_size
        self._y_size = y_size

    def is_point_in_bounds(self, point: Vec2) -> bool:
        """
        Given a Vec2 point, return True if the point lies within the valid board space.

        Arguments:
            point (Vec2):
                The point to validate

        Returns:
            bool (bool):
                Whether or not the point was within the Board bounds.
        """
        # If we wanted to add obstacles, this would be the place to check for potential collisions.
        return (
            point[0] >= 0
            and point[0] <= self._x_size
            and point[1] >= 0
            and point[1] <= self._y_size
        )
