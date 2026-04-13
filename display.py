import sys
import display_render
import write_output
import mazegen.mazegen as mazegen
import random
import bonus


_ANSI_CLEAR_SCREEN = "\033[2J\033[H"
# (wall_color, path_color, logo_color).
COLOR_SCHEMES: list[tuple[str, str, str]] = [
    (
        "\033[38;5;250m",
        "\033[38;5;226m",
        "\033[38;5;196m",
    ),  # light gray + yellow + red
    (
        "\033[38;5;81m",
        "\033[38;5;220m",
        "\033[38;5;201m",
    ),  # cyan + gold + magenta
    (
        "\033[38;5;75m",
        "\033[38;5;118m",
        "\033[38;5;208m",
    ),  # blue + green + orange
    (
        "\033[38;5;45m",
        "\033[38;5;214m",
        "\033[38;5;129m",
    ),  # bright cyan + orange + purple
]


def show_maze(
    maze: "mazegen.MazeGenerator",
    config: dict,
) -> None:
    # kana5do data mn lconfig dict lijbna mn l parsing
    entry = config.get("ENTRY", maze.entry)
    exit_ = config.get("EXIT", maze.exit_)
    output_file: str = config["OUTPUT_FILE"]

    # kan saviw loutput dial lamze f file
    write_output.write_output(maze, output_file)

    # ila kna radi nktbo f file machi terminal
    # maradish ndiro loop and a menu likitsnaw options
    if not sys.stdout.isatty():
        wall_color, path_color, logo_color = COLOR_SCHEMES[0]
        print(
            display_render.render_terminal(
                maze=maze,
                entry=entry,
                exit_=exit_,
                path=None,
                wall_color=wall_color,
                path_color=path_color,
                logo_color=logo_color,
            ),
            flush=True,
        )
        return

    show_path = False
    cached_path: list[tuple[int, int]] | None = None
    scheme_idx = 0
    # main loop dial lproject
    while True:
        # ran 9smo had l pallete of colors into 3 kinds
        wall_color, path_color, logo_color = COLOR_SCHEMES[scheme_idx]

        # path is the list that holds the direction mn start tal end
        # [(start_x, start_y),(x, y),(x, y) ...... , (end_x, end_y)]
        path: list[tuple[int, int]] | None = None
        # show_path boolean false katwli true mni kan5taro option 2
        if show_path:
            # variable kan5biw fiha l path bashmanb9awch n7sboh kola mra
            if cached_path is None:

                cached_path = display_render.path_from_directions(
                    entry,
                    maze.path,
                )
            path = cached_path
        # had str hada kidir (crl + l) awla clear f terminal
        print(_ANSI_CLEAR_SCREEN, end="", flush=True)
        print(
            display_render.render_terminal(
                maze=maze,
                entry=entry,
                exit_=exit_,
                path=path,
                wall_color=wall_color,
                path_color=path_color,
                logo_color=logo_color,
            ),
            flush=True,
        )
        # hada lmenu
        print("\n=== A-maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        # hna kantb3o text wkan handliw ila l
        # program sdinah b (crl + c) wla (crl + d)
        try:
            choice = input("Choice? (1-4): ").strip()
            # option 1 kat3iit 3la generate libdlt fiha
            # kan7iido l path dial lmaze l9dima
            # wkan bdlo data likaina fl output file b maze jdida w path jdid
            if choice == "1":
                maze.generate(random.random())
                cached_path = None
                write_output.write_output(maze, output_file)
                # continue katl3na lfo9 dial l
                # loop bash ntb3o lmaze jdida mn lwl
                continue
            # option 2 katactivi lina l path display wla kat7iido
            if choice == "2":
                show_path = not show_path
                if show_path:
                    if cached_path is None:
                        cached_path = display_render.path_from_directions(
                            entry, maze.path
                        )
                    bonus.animate_path(
                        maze,
                        entry,
                        exit_,
                        cached_path,  # type: ignore
                        wall_color,
                        path_color,
                        logo_color,
                    )
                else:
                    cached_path = None
            # option 3 katbdl lwan liradi nst3mlo lfo9
            if choice == "3":
                scheme_idx = (scheme_idx + 1) % len(COLOR_SCHEMES)
                # continue katl3na lfo9 dial l
                # loop bash ntb3o lmaze jdida mn lwl
                continue

            if choice == "4":
                # creturn katrj mn loop bash lprogram ysali
                return
        except (EOFError, KeyboardInterrupt):
            print()
            return

        print("[!] Invalid choice")
