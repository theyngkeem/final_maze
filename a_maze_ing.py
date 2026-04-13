import sys
import display
from config_parser import iniesta_parser
from mazegen.mazegen import MazeGenerator
from write_output import write_output
from typing import cast


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("try this instead python3 a_maze_ing.py config.txt")
        sys.exit(1)
    try:
        conf = iniesta_parser(sys.argv[1])
        maze = MazeGenerator(
            cast(int, conf["WIDTH"]),
            cast(int, conf["HEIGHT"]),
            cast(tuple[int, int], conf["ENTRY"]),
            cast(tuple[int, int], conf["EXIT"]),
            cast(bool, conf["PERFECT"]),
            cast(int, conf["SEED"]) if conf["SEED"] is not None else None,
        )
        maze.generate()
        display.show_maze(maze, config=conf)
        write_output(maze, conf["OUTPUT_FILE"])
    except BaseException as error:
        print(error)
        sys.exit(1)
