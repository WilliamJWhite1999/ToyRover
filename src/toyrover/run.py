"""
This module serves as the entry-point into the toyrover simulator.
"""

from toyrover.board import Board
from toyrover.input_controller import InputController

BOARD_SIZE = 5.0
""" Default board size to use in the simualtion. """


def run():
    """
    Create a simulation board and input controller. Begin a command loop to accept user input
    indefinitely until the exit command is sent.
    """
    print("Starting ToyRover Simulator.")
    print("Type HELP to see all available commands")

    board = Board(BOARD_SIZE, BOARD_SIZE)
    input_controller = InputController(board)

    should_run = True
    while should_run:
        console_input = str(input("Enter Command > "))
        command, args = input_controller.process_input(console_input)
        if command is not None:
            should_run = input_controller.run_command(command, args)


if __name__ == "__main__":
    run()
