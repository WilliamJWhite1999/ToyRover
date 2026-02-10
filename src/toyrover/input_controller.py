"""
This module contains the InputController, which acts as the central entry point for our simulation.
"""

from pathlib import Path

import numpy as np
from toyrover.board import Board
from toyrover.rover import Rover
from toyrover.types import Command, Direction, Vec2

MOVE_DISTANCE = 1.0
""" Default move distance for movement commands. """

ROTATE_ANGLE = 90.0
""" Default rotation angle for movement commands. """


class InputController:
    """
    The InputController acts as our main object for interacting with the Simulator. It provides
    input management and command execution functionality.

    Pass a string input to the process_input function to generate a tuple containing a Command
    and any args, then pass this result to run_command to execute the command.
    """

    _board: Board
    """ The board that defines the simulation space. """

    _rover: Rover | None
    """ The rover to be simulated. Initially None until a Place command is sent. """

    def __init__(self, board: Board):
        """
        Initialise the InputController.

        Arguments:
            board (Board):
                The board that defines the simulation space.
        """
        self._board = board
        self._rover = None

    def process_input(self, input: str) -> tuple[Command | None, str | None]:
        """
        Given a string input of format COMMAND ARGUMENTS, return the corresponding Command enum
        and the arguments. The results of this should be passed to run_command to execute the
        command when ready.

        Arguments:
            input (str):
                Input to be processed into the internal command format.

        Returns:
            command: tuple[Command, str | None]:
                Tuple containing the Command enum and any arguments (if present).
        """
        cleaned_input = input.strip()
        input_pieces = cleaned_input.split(" ")

        assert (
            len(input_pieces) <= 2
        ), "Input format should be `<COMMAND>` or `<COMMAND> <ARGS>`"

        try:
            command = Command(input_pieces[0].upper())
        except ValueError:
            # Not sure on desired failure criteria, so assume we choose to ignore mangled commands.
            print(
                f"Cannot interpret input '{input_pieces[0]}' as a command Command must be one of "
                f"{list(Command)}."
            )
            return None, None

        args = input_pieces[1] if len(input_pieces) == 2 else None

        return command, args

    def _handle_file(self, path: str | Path):
        """
        Given a filepath, load the file and run each line in the file as if it were a command to
        be executed

        Arguments:
            path (str | Path):
                String or path object representing the filepath to the file to be loaded.
        """
        filepath = Path(path)
        if not filepath.is_file():
            # Safe failure mode.
            print(f"Filepath {filepath} is not a valid file.")
            return

        with open(filepath, "r") as fh:
            for line in fh.readlines():
                command, args = self.process_input(line)
                if command is not None:
                    self.run_command(command, args)

    def _handle_place(self, args: str):
        """
        Try to place the rover at the provided position with the given orientation. If the
        provided point is out of bounds, this will be ignored.

        Arguments:
            args (str):
                position and orientation in the format: x,y,direction where direction is one of
                "NORTH", "EAST", "SOUTH" or "WEST"
        """
        place_args = args.split(",")

        if len(place_args) != 3:
            print(f"Expected 3 comma-separated values for place command, got '{args}'.")
            return

        position: Vec2 = np.array(
            [float(place_args[0]), float(place_args[1])], dtype=np.float64
        )
        direction = Direction(place_args[2].upper()).as_vec2()

        # Handle rover creation here so if we *wanted* to it would be very easy to have
        # multiple rovers spin up via input.
        if self._rover is None:
            if self._board.is_point_in_bounds(position):
                self._rover = Rover(self._board, position, direction)
            else:
                print(f"Unable to create rover at {position} as this is out of bounds.")

        else:
            self._rover.place(position, direction)

    def run_command(self, command: Command, args: str | None = None) -> bool:
        """
        Given a command and optionally some arguments for the command, execute the given command.
        Returns True upon command completion unless the EXIT command is triggered in which case
        return False.

        Arguments:
            command: Command
                The command to be executed
            args: str | None
                Any arguments necessary for the command. The FILE and PLACE commands require
                arguments.
        """
        match command:
            case Command.FILE:
                assert args is not None, f"Arguments are required for command {command}"
                self._handle_file(args)

            case Command.PLACE:
                assert args is not None, f"Arguments are required for command {command}"
                self._handle_place(args)

            case Command.MOVE:
                # If desired, could add argument for move amount
                if self._rover is not None:
                    self._rover.move(MOVE_DISTANCE)
                else:
                    print("No rover present, place a rover first!")

            case Command.LEFT:
                # If desired, could add argument for rotation amount
                if self._rover is not None:
                    self._rover.rotate_left(ROTATE_ANGLE)
                else:
                    print("No rover present, place a rover first!")

            case Command.RIGHT:
                # If desired, could add argument for rotation amount
                if self._rover is not None:
                    self._rover.rotate_right(ROTATE_ANGLE)
                else:
                    print("No rover present, place a rover first!")

            case Command.REPORT:
                if self._rover is not None:
                    self._rover.report()
                else:
                    print("No rover present, place a rover first!")

            case Command.HELP:
                print("List of commands:")
                for command in Command:
                    print(f"\t{command.value}\t{command.doc}")

            case Command.EXIT:
                return False

            case _:
                # Shouldn't be possible to hit this since we have defined all our Command types,
                # but if this were extended to have new Commands we might hit this path.
                print(f"Error: Command {command} not supported.")

        return True
