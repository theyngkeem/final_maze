from __future__ import annotations

import mazegen.mazegen as mazegen

import display_draw


# had lfunction katchd lina l path (str) li kain f mazegen wkatrj3o lista
# st3mlnaha f display
def path_from_directions(
    start: tuple[int, int],
    directions: str,
) -> list[tuple[int, int]] | None:
    x, y = start
    out: list[tuple[int, int]] = [(x, y)]
    for ch in directions or "":
        if ch == "N":
            y -= 1
        elif ch == "S":
            y += 1
        elif ch == "E":
            x += 1
        elif ch == "W":
            x -= 1
        else:
            return None
        out.append((x, y))
    return out


# function likat tb3 lina l maze 3iitna liha f display
def render_terminal(
    maze: mazegen.MazeGenerator,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[tuple[int, int]] | None,
    wall_color: str,
    path_color: str,
    logo_color: str,
    wall_char: str = "█",
) -> str:
    # lmaze kayn f mazegen w table hiya l 2d list li katmatal lmaze
    table = maze.table
    height = len(table)
    width = len(table[0])

    # hadi katjib lina logo_cells wkat7thom
    # f set bashmanb9awch n7sbohom kola mra
    logo_cells: set = getattr(maze, "logo_cells", set())

    # function wash had cell hiya logo wla la
    def is_logo(x: int, y: int) -> bool:
        if not (0 <= x < width and 0 <= y < height):
            return False
        if (x, y) == entry or (x, y) == exit_:
            return False
        return (x, y) in logo_cells

    # ila kan path ma3tina kanrdoh set tahowa
    # bash manb9awch n7sboh kola mra f display_draw
    path_set = set(path) if path else set()
    # hna kanjm3o lwalls li7iidna mabin kola cell
    # w cell fl path bash nlwnohom bl color dial path mnb3d
    h_edges: set[tuple[int, int]] = set()
    v_edges: set[tuple[int, int]] = set()
    if path and len(path) >= 2:
        for (x, y), (nx, ny) in zip(path, path[1:]):
            if nx == x + 1 and ny == y:
                h_edges.add((x, y))
            elif nx == x - 1 and ny == y:
                h_edges.add((nx, ny))
            elif nx == x and ny == y + 1:
                v_edges.add((x, y))
            elif nx == x and ny == y - 1:
                v_edges.add((nx, ny))

    lines = display_draw.build_terminal_lines(
        table,
        entry=entry,
        exit_=exit_,
        is_logo=is_logo,
        path_set=path_set,
        h_edges=h_edges,
        v_edges=v_edges,
        wall_char=wall_char,
        wall_color=wall_color,
        path_color=path_color,
        logo_color=logo_color,
    )

    return "\n".join(lines)
