"""
This module contains the Rover, which is the simulated entity in this simulator. It has basic
movement and rotation functionality.
"""

import numpy as np
from toyrover.board import Board
from toyrover.types import Direction, Vec2


class Rover:
    """
    The Rover is a simulated entity with basic movement and rotation functionality.
    """

    _board: Board
    """
    The board that this Rover exists upon. Used to validate the Rover remains in the world space
    """

    _position: Vec2
    """ Current position vector relative to the south-west corner of the board. """

    _direction: Vec2
    """ Unit vector direction of the rover. """

    def __init__(self, board: Board, position: Vec2, direction: Vec2):
        """
        Initialise the Rover with a parent Board and start position and direction.

        Arguments:
            board (Board):
                The board that this Rover exists on.
            position (Vec2):
                Starting position of the Rover.
            direction (Vec2):
                Starting direction of the Rover as a vector.
        """
        self._board = board
        if not self._board.is_point_in_bounds(position):
            raise ValueError("Position must be valid for Rover initialisation.")
        self.place(position, direction)

    def get_position(self) -> Vec2:
        """Return a copy of the position vector to prevent mutation"""
        return self._position.copy()

    def get_direction(self) -> Vec2:
        """Return a copy of the direction vector to prevent mutation"""
        return self._direction.copy()

    def place(self, position: Vec2, direction: Vec2):
        """
        Place the Rover at the given position with the given direction vector. If the position is
        invalid then this update will be ignored.

        Arguments:
            position (Vec2):
                Position vector to update the Rover to.
            direction (Vec2):
                Direction vector to update the Rover to.
        """
        if self._board.is_point_in_bounds(position):
            self._position = position
            # Ensure direction is a unit vector.
            self._direction = direction / np.linalg.norm(direction)
        else:
            print(f"Point {position} is out of bounds. Place action ignored.")

    def move(self, distance: float):
        """
        Move the Rover in its direction heading by the given amount of units.
        """
        target_pos = self._position + self._direction * distance
        if self._board.is_point_in_bounds(target_pos):
            self._position = target_pos
        else:
            print(f"Cannot move {distance} units as would move rover out of bounds!")

    def _get_rot_matrix(self, angle_deg: float) -> np.ndarray:
        """
        Utility function to get the 2D rotation matrix for the given angle. Assumes
        counter-clockwise is positive.
        """
        angle_rad = np.radians(angle_deg)
        return np.array(
            [
                [np.cos(angle_rad), -np.sin(angle_rad)],
                [np.sin(angle_rad), np.cos(angle_rad)],
            ]
        )

    def rotate_left(self, angle_deg: float):
        """
        Rotate the rover left by the given angle measured in degrees.
        """
        rot_mat = self._get_rot_matrix(angle_deg)
        self._direction = rot_mat @ self._direction

    def rotate_right(self, angle_deg: float):
        """
        Rotate the rover right by the given angle measured in degrees.
        """
        rot_mat = self._get_rot_matrix(-angle_deg)
        self._direction = rot_mat @ self._direction

    def _coerce_direction_to_cardinal(
        self, tolerance: float = 1e-6
    ) -> Direction | None:
        """
        Convert the Rover's direction vector into the closest available Direction vector as long as
        this is within some tolerance. The main purpose of this function is to allow us to represent
        direction as an arbitrary vector, but later convert it to our Direction types for prettier
        printing when available.
        """
        all_dirs = list(Direction)
        all_dir_vals = np.vstack([direction.as_vec2() for direction in all_dirs])
        dir_distance = np.sum(
            np.abs(all_dir_vals - self._direction[np.newaxis, :]), axis=1
        )
        closest_dir_idx = np.argmin(dir_distance)

        if dir_distance[closest_dir_idx] <= tolerance:
            return all_dirs[closest_dir_idx]
        else:
            return None

    def report(self):
        """
        Print the current rover position and direction.
        """
        if cardinal_dir := self._coerce_direction_to_cardinal():
            direction = cardinal_dir
        else:
            direction = self._direction

        print(
            f"Rover Position: {self._position[0]:.2f}, {self._position[1]:.2f}, "
            f"Direction: {direction}"
        )
