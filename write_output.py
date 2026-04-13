from mazegen.mazegen import MazeGenerator


def write_output(maze: MazeGenerator, path: str) -> None:
    """write the output in hex format"""
    with open(path, 'w') as file:
        for row in maze.table:
            for c in row:
                file.write(f"{c:X}")
            file.write('\n')
        file.write("\n")
        ecol, erow = maze.entry
        xcol, xrow = maze.exit_
        file.write(f"{ecol},{erow}\n")
        file.write(f"{xcol},{xrow}\n")
        file.write(f"{maze.path}\n")
