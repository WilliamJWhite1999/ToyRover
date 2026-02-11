from functools import partial
from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
from toyrover.input_controller import InputController
from toyrover.types import Command, Direction, PlaceArgs


def assert_place_args_match(expected: PlaceArgs, observed: PlaceArgs):
    """
    Assert that the two PlaceArgs objects are within floating-point precision bounds.
    """
    assert np.allclose(expected.position, observed.position)
    assert np.allclose(expected.direction, observed.direction)


def test_process_input(tmp_path):
    """
    Test various valid inputs that should return a command and arguments correctly.
    """
    input_controller = InputController(MagicMock())

    dummy_file_path = Path(f"{tmp_path}/dummy_file.txt")
    with open(dummy_file_path, "w") as fh:
        fh.write("\n")

    command = f"FILE {dummy_file_path}"
    output_command, output_args = input_controller.process_input(command)
    expected_command = Command.FILE
    expected_args = dummy_file_path
    assert expected_command == output_command
    assert isinstance(output_args, Path)
    assert expected_args == output_args

    command = "PLACE 1,1,NORTH"
    output_command, output_args = input_controller.process_input(command)
    expected_command = Command.PLACE
    expected_pos = np.array([1, 1])
    expected_dir = Direction.NORTH.as_vec2()
    assert expected_command == output_command
    assert isinstance(output_args, PlaceArgs)
    assert np.allclose(expected_pos, output_args.position)
    assert np.allclose(expected_dir, output_args.direction)

    command = "MOVE"
    output_command, output_args = input_controller.process_input(command)
    expected_command = Command.MOVE
    expected_args = None
    assert expected_command == output_command
    assert expected_args == output_args

    command = "LEFT"
    output_command, output_args = input_controller.process_input(command)
    expected_command = Command.LEFT
    expected_args = None
    assert expected_command == output_command
    assert expected_args == output_args

    # Try some with varied capitalisation
    command = "riGHt"
    output_command, output_args = input_controller.process_input(command)
    expected_command = Command.RIGHT
    expected_args = None
    assert expected_command == output_command
    assert expected_args == output_args

    command = "REpoRT"
    output_command, output_args = input_controller.process_input(command)
    expected_command = Command.REPORT
    expected_args = None
    assert expected_command == output_command
    assert expected_args == output_args

    # And some with leading and trailing spaces
    command = "  help"
    output_command, output_args = input_controller.process_input(command)
    expected_command = Command.HELP
    expected_args = None
    assert expected_command == output_command
    assert expected_args == output_args

    command = "  EXIT  "
    output_command, output_args = input_controller.process_input(command)
    expected_command = Command.EXIT
    expected_args = None
    assert expected_command == output_command
    assert expected_args == output_args


def test_process_input_malformed():
    """
    Test various invalid inputs that should not return a command at all.
    """
    input_controller = InputController(MagicMock())

    expected_command = None
    expected_args = None

    # Invalid command type
    command = "xxxx"
    output_command, output_args = input_controller.process_input(command)
    assert expected_command == output_command
    assert expected_args == output_args

    command = "riGHtt"
    output_command, output_args = input_controller.process_input(command)
    assert expected_command == output_command
    assert expected_args == output_args

    # Invalid args
    command = f"FILE missing_file.txt"
    output_command, output_args = input_controller.process_input(command)
    assert expected_command == output_command
    assert expected_args == output_args

    command = "PLACE 1,1,NORTH,1"
    output_command, output_args = input_controller.process_input(command)
    assert expected_command == output_command
    assert expected_args == output_args

    command = "PLACE 1,1,WEAST,1"
    output_command, output_args = input_controller.process_input(command)
    assert expected_command == output_command
    assert expected_args == output_args

    command = "PLACE 1,1"
    output_command, output_args = input_controller.process_input(command)
    assert expected_command == output_command
    assert expected_args == output_args

    command = "PLACE Cake,1,NORTH"
    output_command, output_args = input_controller.process_input(command)
    assert expected_command == output_command
    assert expected_args == output_args


def test_exit_command():
    """
    Assert that running the exit command returns False.
    """
    input_controller = InputController(MagicMock())
    assert input_controller.run_command(Command.EXIT) is False


def test_file_command(tmp_path):
    """
    Test various valid inputs that should return a command and arguments correctly.
    """
    input_controller = InputController(MagicMock())

    # Mock out the place command, we'll use this command in our file to check that the commands are
    # being called correctly.

    place_calls: list[PlaceArgs] = []

    def record_place(_, place_args: PlaceArgs):
        place_calls.append(place_args)

    input_controller._handle_place = partial(record_place, input_controller)

    dummy_file_path = Path(f"{tmp_path}/dummy_file.txt")
    with open(dummy_file_path, "w") as fh:
        fh.write("PLACE 1,1,NORTH\n")
        fh.write("PLACE 1,3,NORTH\n")
        fh.write("PLACE -1,1,SOUTH\n")
        fh.write("PLACE 0,5,WEST\n")
        fh.write("PLACE 0,5,WEAST\n")  # Malformed - expect it is not present
        fh.write("MALFORMED\n")  # Malformed - expect it is not present

    input_controller.run_command(Command.FILE, dummy_file_path)

    assert len(place_calls) == 4

    expected_args_1 = PlaceArgs(
        position=np.array([1, 1]), direction=Direction.NORTH.as_vec2()
    )
    assert_place_args_match(expected_args_1, place_calls[0])

    expected_args_2 = PlaceArgs(
        position=np.array([1, 3]), direction=Direction.NORTH.as_vec2()
    )
    assert_place_args_match(expected_args_2, place_calls[1])

    expected_args_3 = PlaceArgs(
        position=np.array([-1, 1]), direction=Direction.SOUTH.as_vec2()
    )
    assert_place_args_match(expected_args_3, place_calls[2])

    expected_args_4 = PlaceArgs(
        position=np.array([0, 5]), direction=Direction.WEST.as_vec2()
    )
    assert_place_args_match(expected_args_4, place_calls[3])


# NOTE: Rover commands are handled in system test.
