from typing import Callable

import mazegen.mazegen as mazegen


Coord = tuple[int, int]
IsLogoFn = Callable[[int, int], bool]

# hadi bash nrj3o white color f terminal kanst3mloha f print()
_RESET = "\033[0m"


def build_terminal_lines(
    table: list[list[int]],
    entry: Coord,
    exit_: Coord,
    is_logo: IsLogoFn,
    path_set: set[Coord],
    h_edges: set[Coord],
    v_edges: set[Coord],
    wall_char: str,
    wall_color: str,
    path_color: str,
    logo_color: str,
) -> list[str]:

    def paint(text: str, color: str) -> str:
        return f"{color}{text}{_RESET}"

    height = len(table)
    width = len(table[0])
    wall3 = wall_char * 3
    space3 = " " * 3

    def logo_at(x: int, y: int) -> bool:
        if 0 <= x < width and 0 <= y < height:
            return is_logo(x, y)
        return False

    def on_path(x: int, y: int) -> bool:
        return (x, y) in path_set

    def path_marker(ch: str) -> str:
        return paint(wall_char, path_color) + ch + paint(wall_char, path_color)

    def cell_body(x: int, y: int, cur_is_logo: bool) -> str:
        if cur_is_logo:
            return paint(wall3, logo_color)

        if (x, y) == entry:
            return path_marker("S") if on_path(x, y) else " S "
        if (x, y) == exit_:
            return path_marker("E") if on_path(x, y) else " E "

        if on_path(x, y):
            return paint(wall3, path_color)
        return space3

    def left_wall(x: int, y: int, mask: int, cur_is_logo: bool) -> str:
        wall_is_logo = cur_is_logo or logo_at(x - 1, y)
        if mask & mazegen.WEST:
            return paint(
                wall_char,
                logo_color if wall_is_logo else wall_color,
            )
        if (x - 1, y) in h_edges:
            return paint(wall_char, path_color)
        return " "

    def right_wall(y: int) -> str:
        last_mask = table[y][width - 1]
        if last_mask & mazegen.EAST:
            return paint(
                wall_char,
                logo_color if logo_at(width - 1, y) else wall_color,
            )
        return " "

    def corner_has_logo(x: int, y: int) -> bool:
        return (
            logo_at(x, y)
            or logo_at(x - 1, y)
            or logo_at(x, y + 1)
            or logo_at(x - 1, y + 1)
        )

    def row_line(y: int) -> str:
        parts: list[str] = []
        for x in range(width):
            mask = table[y][x]
            cur_is_logo = logo_at(x, y)
            parts.append(left_wall(x, y, mask, cur_is_logo))
            parts.append(cell_body(x, y, cur_is_logo))
        parts.append(right_wall(y))
        return "".join(parts)

    def bottom_line(y: int) -> str:
        parts: list[str] = []
        for x in range(width):
            mask = table[y][x]

            parts.append(
                paint(
                    wall_char,
                    logo_color if corner_has_logo(x, y) else wall_color,
                )
            )

            cell_is_logo = logo_at(x, y)
            below_is_logo = logo_at(x, y + 1)
            if mask & mazegen.SOUTH:
                parts.append(
                    paint(
                        wall3,
                        logo_color if (cell_is_logo or below_is_logo) else
                        wall_color,
                    )
                )
            elif (x, y) in v_edges:
                parts.append(paint(wall3, path_color))
            else:
                parts.append(space3)

        parts.append(
            paint(
                wall_char,
                logo_color if corner_has_logo(width, y) else wall_color,
            )
        )
        return "".join(parts)

    # hada howa awal str kiban, lcadre lfo9ani
    lines: list[str] = [paint(wall_char * (width * 4 + 1), wall_color)]
    # had loop rabania hia li kat5bi lina lines liradi ytb3o f terminal
    # wa7d b wa7d
    for y in range(height):
        lines.append(row_line(y))
        lines.append(bottom_line(y))

    return lines
