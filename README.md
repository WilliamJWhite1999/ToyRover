# ToyRover
Toy Rover demo project

# Starting Up
This project has been created to use UV as its package manager. Installing UV is detailed
[here](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1), but the section
'Installing UV' outlines the necessary steps. Once installed a terminal restart is required.

Once UV is installed, the project dependencies can be acquired by running `uv sync`. The program
can then be run by executing `uv run main`.

Alternatively, a requirements.txt has been provided if you wish to directly install the project's
dependencies to an existing environment. The only dependency is Numpy 2.

# Commands
The set of available commands in the simulator is detailed below:
- `FILE`    Read commands from the provided filepath. Accepts one arg in the form of a filepath.
- `PLACE`   Place the rover at the specified x,y coordinates with given direction. Accepts one arg
in the form x,y,Direction e.g. 1,3,NORTH
- `MOVE`    Move the rover one place forwards.
- `LEFT`    Rotate the rover 90 degrees to the left.
- `RIGHT`   Rotate the rover 90 degrees to the right.
- `REPORT`  Display the current location of the rover.
- `HELP`    Display a help message.
- `EXIT`    Exit the simulator.

# Installing UV
Windows
- `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Linux
- `curl -LsSf https://astral.sh/uv/install.sh | sh`