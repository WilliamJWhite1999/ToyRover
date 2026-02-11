"""
This module contains the InputController, which acts as the central entry point for our simulation.
"""

from pathlib import Path

import numpy as np
from toyrover.board import Board
from toyrover.rover import Rover
from toyrover.types import Command, Direction, PlaceArgs, Vec2

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

    def process_input(
        self, input: str
    ) -> tuple[Command | None, Path | PlaceArgs | None]:
        """
        Given a string input of format COMMAND ARGUMENTS, return the corresponding Command enum
        and the arguments. The results of this should be passed to run_command to execute the
        command when ready.

        Arguments:
            input (str):
                Input to be processed into the internal command format.

        Returns:
            command: tuple[Command, Path | PlaceArgs | None]:
                Tuple containing the Command enum and any arguments (if present).
        """
        # Clean input
        cleaned_input = input.strip()
        if len(cleaned_input) == 0:
            # Silent exit on empty command
            return None, None

        input_pieces = cleaned_input.split(" ")

        # All commands are of form <Command> or <Command> <Args>, if the input doesn't match this
        # then break early.
        if len(input_pieces) != 1 and len(input_pieces) != 2:
            print("Input format should be `<COMMAND>` or `<COMMAND> <ARGS>`")
            return None, None

        # Extract Command type.
        try:
            command = Command(input_pieces[0].upper())
        except ValueError:
            # Not sure on desired failure criteria, so assume we choose to ignore mangled commands.
            print(
                f"Cannot interpret input '{input_pieces[0]}' as a command Command must be one of "
                f"{list(Command)}."
            )
            return None, None

        # Extract command args.
        try:
            match command:
                case Command.FILE:
                    args = Path(input_pieces[1])
                    if not args.is_file():
                        raise ValueError(f"Filepath {args} is not a valid file.")

                case Command.PLACE:
                    place_args = input_pieces[1].split(",")

                    if len(place_args) != 3:
                        raise ValueError(
                            f"Unable to interpret {input_pieces[1]} as valid placement args. "
                            "Expected form x,y,direction"
                        )

                    position: Vec2 = np.array(
                        [float(place_args[0]), float(place_args[1])], dtype=np.float64
                    ).astype(np.float64)
                    direction = Direction(place_args[2].upper()).as_vec2()

                    args = PlaceArgs(position, direction)

                case _:
                    args = None

        except ValueError:
            # Gracefully exit on malformed args
            print(
                f"Unable to interpret args '{input_pieces[1]}' for command '{command}'"
            )
            return None, None

        return command, args

    def _handle_file(self, filepath: Path):
        """
        Given a filepath, load the file and run each line in the file as if it were a command to
        be executed

        Arguments:
            path (str | Path):
                String or path object representing the filepath to the file to be loaded.
        """
        with open(filepath, "r") as fh:
            for line in fh.readlines():
                command, args = self.process_input(line)
                if command is not None:
                    self.run_command(command, args)

    def _handle_place(self, place_args: PlaceArgs):
        """
        Try to place the rover at the provided position with the given orientation. If the
        provided point is out of bounds, this will be ignored.

        Arguments:
            args (str):
                position and orientation in the format: x,y,direction where direction is one of
                "NORTH", "EAST", "SOUTH" or "WEST"
        """
        # Handle rover creation here so if we *wanted* to it would be very easy to have
        # multiple rovers spin up via input.
        if self._rover is None:
            if self._board.is_point_in_bounds(place_args.position):
                self._rover = Rover(
                    self._board, place_args.position, place_args.direction
                )
            else:
                print(
                    f"Unable to create rover at {place_args.position} as this is out of bounds."
                )

        else:
            self._rover.place(place_args.position, place_args.direction)

    def run_command(
        self, command: Command, args: Path | PlaceArgs | None = None
    ) -> bool:
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
                assert isinstance(
                    args, Path
                ), f"Arguments are required for command {command}"
                self._handle_file(args)

            case Command.PLACE:
                assert isinstance(
                    args, PlaceArgs
                ), f"Arguments are required for command {command}"
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
