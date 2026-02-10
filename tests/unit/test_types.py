import numpy as np
from toyrover.types import Command, Direction


def test_command_conversions():
    """
    Test that our Command enum correctly interprets input strings as Commands
    """
    assert Command("FILE") == Command.FILE
    assert Command("PLACE") == Command.PLACE
    assert Command("MOVE") == Command.MOVE
    assert Command("LEFT") == Command.LEFT
    assert Command("RIGHT") == Command.RIGHT
    assert Command("REPORT") == Command.REPORT
    assert Command("HELP") == Command.HELP
    assert Command("EXIT") == Command.EXIT


def test_direction_conversions():
    """
    Test that our Direction enum correctly interprets input strings as Directions
    """
    assert Direction("NORTH") == Direction.NORTH
    assert Direction("EAST") == Direction.EAST
    assert Direction("SOUTH") == Direction.SOUTH
    assert Direction("WEST") == Direction.WEST


def test_direction_vectors():
    """
    Assert that all Direction vectors have a corresponding Vec2. They should each be unique and
    of unit magnitude
    """
    tolerance = 1e-12
    num_dirs = 4

    # All vectors should be unit vectors.
    assert np.abs(np.linalg.norm(Direction.NORTH.as_vec2())) - 1 < tolerance
    assert np.abs(np.linalg.norm(Direction.EAST.as_vec2())) - 1 < tolerance
    assert np.abs(np.linalg.norm(Direction.SOUTH.as_vec2())) - 1 < tolerance
    assert np.abs(np.linalg.norm(Direction.WEST.as_vec2())) - 1 < tolerance

    # Count unique rows, expect as many as number of directions
    assert (
        np.unique(
            [tuple(direction.as_vec2().tolist()) for direction in Direction], axis=0
        ).shape[0]
        == num_dirs
    )
