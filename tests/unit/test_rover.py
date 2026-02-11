import re
import numpy as np
import pytest

from toyrover.board import Board
from toyrover.rover import Rover
from toyrover.types import Direction


def create_board(x_size: float = 5, y_size: float = 5) -> Board:
    """
    Create a simple board for tests
    """
    return Board(x_size, y_size)


def test_rover_place_oob():
    """
    Attempt to create a rover out of bounds, assert that this raises an error.
    Place the rover and assert that its position and direction reflect the input values.
    Attempt to then place the rover oob again and assert that no change is reflected.
    Place the rover one final time at a different valid location and assert a change is made.
    """
    board = create_board()

    oob_position = np.array([10, 10])
    valid_position = np.array([3, 3])
    direction = np.array([1, 0])

    # Place out of bounds, assert raises an error
    with pytest.raises(ValueError):
        rover = Rover(board, oob_position, direction)

    # Place in bounds, if no error is raised then the test passes.
    rover = Rover(board, valid_position, direction)
    assert np.allclose(rover.get_position(), valid_position)
    assert np.allclose(rover.get_direction(), direction)

    rover.place(oob_position, direction)
    assert np.allclose(rover.get_position(), valid_position)
    assert np.allclose(rover.get_direction(), direction)

    valid_position_2 = np.array([1, 4])
    rover.place(valid_position_2, direction)
    assert np.allclose(rover.get_position(), valid_position_2)
    assert np.allclose(rover.get_direction(), direction)


def test_rover_move():
    """
    Create a rover and move it forward. Assert that the rover moves in the expected direction.
    Attempt to move out of bounds and assert that the rover does not leave the board.
    """
    board = create_board()

    move_distance = 1.0

    start_position = np.array([3, 3])
    direction = Direction.EAST.as_vec2()

    # Place in bounds, if no error is raised then the test passes.
    rover = Rover(board, start_position, direction)

    # Start at 3, Boundary at 5 - expect to be able to move twice before unable to move further
    expected_pos_1 = np.array([4, 3])
    rover.move(move_distance)
    assert np.allclose(rover.get_position(), expected_pos_1)

    expected_pos_2 = np.array([5, 3])
    rover.move(move_distance)
    assert np.allclose(rover.get_position(), expected_pos_2)

    # Expect no change since already at the boundary.
    expected_pos_3 = np.array([5, 3])
    rover.move(move_distance)
    assert np.allclose(rover.get_position(), expected_pos_3)


def test_rover_rotate():
    """
    Create a rover. Rotate it in 90 degree increments several times and assert that the rotations
    proceed as expected.
    """
    board = create_board()

    rotate_amount = 90.0

    start_position = np.array([3, 3])
    direction = Direction.EAST.as_vec2()

    # Place in bounds, if no error is raised then the test passes.
    rover = Rover(board, start_position, direction)

    expected_rotation = Direction.NORTH.as_vec2()
    rover.rotate_left(rotate_amount)
    assert np.allclose(rover.get_direction(), expected_rotation)

    expected_rotation = Direction.WEST.as_vec2()
    rover.rotate_left(rotate_amount)
    assert np.allclose(rover.get_direction(), expected_rotation)

    expected_rotation = Direction.SOUTH.as_vec2()
    rover.rotate_left(rotate_amount)
    assert np.allclose(rover.get_direction(), expected_rotation)

    expected_rotation = Direction.WEST.as_vec2()
    rover.rotate_right(rotate_amount)
    assert np.allclose(rover.get_direction(), expected_rotation)

    expected_rotation = Direction.NORTH.as_vec2()
    rover.rotate_right(rotate_amount)
    assert np.allclose(rover.get_direction(), expected_rotation)

    expected_rotation = Direction.EAST.as_vec2()
    rover.rotate_right(rotate_amount)
    assert np.allclose(rover.get_direction(), expected_rotation)


def test_rover_report(capsys):
    """
    Create a Rover, report its current position and assert that something matching the expected
    output format was printed. Move the Rover and repeat.
    """
    board = create_board()

    start_position = np.array([3, 3])
    direction = Direction.EAST.as_vec2()

    # Place in bounds, if no error is raised then the test passes.
    rover = Rover(board, start_position, direction)

    rover.report()
    captured, err = capsys.readouterr()

    assert len(err) == 0, "Expected no errors."
    assert len(captured) > 0
    assert re.match("Rover Position: [\d.]+, [\d.]+", captured) is not None
    assert "Direction: EAST" in captured

    new_direction = Direction.SOUTH.as_vec2()

    rover.place(start_position, new_direction)

    rover.report()
    captured, err = capsys.readouterr()

    assert len(err) == 0, "Expected no errors."
    assert len(captured) > 0
    assert re.match("Rover Position: [\d.]+, [\d.]+", captured) is not None
    assert "Direction: SOUTH" in captured
