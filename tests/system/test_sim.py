import re

import numpy as np
from toyrover.board import Board
from toyrover.input_controller import InputController


def test_sim_system(capsys):
    """
    Start out of bounds, try to move but this should do nothing, then place successfully and move
    away.

    System test so interact with the system as a user would, i.e. extracting results from the
    terminal.

    Validates the input controller's entry point for commands and its ability to output in an
    expected format to the user.
    """
    board = Board(5, 5)
    input_controller = InputController(board)

    # Place a rover out of bounds - assert that an error message is reported but no data.
    input_controller.process_and_run_input("PLACE 7,3,NORTH")
    input_controller.process_and_run_input("REPORT")
    captured, err = capsys.readouterr()
    assert len(err) == 0, "Expected no errors."
    assert len(captured) > 0
    assert "No rover present" in captured
    assert "Rover Position: " not in captured
    assert "Direction: " not in captured

    # Now place in bounds and assert that something is reported
    expected_x = 3.0
    expected_y = 3.0
    expected_dir = "NORTH"
    command = f"PLACE {expected_x},{expected_y},{expected_dir}"

    input_controller.process_and_run_input(command)
    input_controller.process_and_run_input("REPORT")

    # Extract rover position and direction from report output
    captured, err = capsys.readouterr()
    capture_pos = re.match(r"Rover Position: ([\d.]+), ([\d.]+)", captured)
    x, y = float(capture_pos.group(1)), float(capture_pos.group(2))

    assert np.isclose(expected_x, x)
    assert np.isclose(expected_y, y)
    assert f"Direction: {expected_dir}" in captured

    # Move the Rover to assert it continues behaves as expected
    # One North, Left, Two West i.e. move from (3,3) -> (1,4)
    input_controller.process_and_run_input("MOVE")
    input_controller.process_and_run_input("LEFT")
    input_controller.process_and_run_input("MOVE")
    input_controller.process_and_run_input("MOVE")
    input_controller.process_and_run_input("REPORT")

    expected_x = 1.0
    expected_y = 4.0
    expected_dir = "WEST"

    # Extract rover position and direction from report output
    captured, err = capsys.readouterr()
    capture_pos = re.match(r"Rover Position: ([\d.]+), ([\d.]+)", captured)
    x, y = float(capture_pos.group(1)), float(capture_pos.group(2))

    assert np.isclose(expected_x, x)
    assert np.isclose(expected_y, y)
    assert f"Direction: {expected_dir}" in captured

    # Continue moving the rover until is should go out of bounds, assert that it doesn't
    # Move Two West and Two North i.e. (1,4) -> (-1, 6) but this is out of bounds so should see
    # (0, 5) as our end position
    input_controller.process_and_run_input("MOVE")
    input_controller.process_and_run_input("MOVE")
    input_controller.process_and_run_input("RIGHT")
    input_controller.process_and_run_input("MOVE")
    input_controller.process_and_run_input("MOVE")
    input_controller.process_and_run_input("REPROT")

    expected_x = 0.0
    expected_y = 5.0
    expected_dir = "NORTH"

    # Extract rover position and direction from report output
    captured, err = capsys.readouterr()
    capture_pos = re.match(r"Rover Position: ([\d.]+), ([\d.]+)", captured)
    x, y = float(capture_pos.group(1)), float(capture_pos.group(2))

    assert np.isclose(expected_x, x)
    assert np.isclose(expected_y, y)
    assert f"Direction: {expected_dir}" in captured
