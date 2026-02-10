import numpy as np
from toyrover.board import Board


def test_board_bounds():
    """
    Create a board, assert that any point in or along the bounds is counted as being within the
    board boundary while any beyond it in any direction are not.
    """
    x_max = 5
    y_max = 3

    board = Board(x_max, y_max)

    # Check all boundary points are valid
    valid_p1 = np.array([0, 0])
    valid_p2 = np.array([x_max, 0])
    valid_p3 = np.array([0, y_max])
    valid_p4 = np.array([x_max, y_max])

    assert board.is_point_in_bounds(valid_p1)
    assert board.is_point_in_bounds(valid_p2)
    assert board.is_point_in_bounds(valid_p3)
    assert board.is_point_in_bounds(valid_p4)

    # Check some central points are valid
    valid_p5 = np.array([x_max, 1])
    valid_p6 = np.array([3, y_max])
    valid_p7 = np.array([1, 1])
    valid_p8 = np.array([4, 1])

    assert board.is_point_in_bounds(valid_p5)
    assert board.is_point_in_bounds(valid_p6)
    assert board.is_point_in_bounds(valid_p7)
    assert board.is_point_in_bounds(valid_p8)

    # Check points beyond or multiple bounds are invalid
    invalid_p1 = np.array([-1, -1])
    invalid_p2 = np.array([-1, 1])
    invalid_p3 = np.array([3, -1])
    invalid_p4 = np.array([x_max + 1, 1])
    invalid_p5 = np.array([4, y_max + 1])
    invalid_p6 = np.array([x_max + 1, y_max + 1])

    assert not board.is_point_in_bounds(invalid_p1)
    assert not board.is_point_in_bounds(invalid_p2)
    assert not board.is_point_in_bounds(invalid_p3)
    assert not board.is_point_in_bounds(invalid_p4)
    assert not board.is_point_in_bounds(invalid_p5)
    assert not board.is_point_in_bounds(invalid_p6)
