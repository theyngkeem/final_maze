import time
import display_render

CLEAR_SCREEN = "\033[2J\033[H"


def animate_path(maze, entry: tuple[int, int], exit_: tuple[int, int],
                 full_path: list, wall_color: str,
                 path_color: str, logo_color: str,
                 delay: float = 0.04,) -> None:
    """Reveal the solution path step by step."""
    for i in range(1, len(full_path) + 1):
        print(CLEAR_SCREEN, end="", flush=True)
        print(display_render.render_terminal(maze=maze, entry=entry,
                                             exit_=exit_,
                                             path=full_path[:i],
                                             wall_color=wall_color,
                                             path_color=path_color,
                                             logo_color=logo_color))
        time.sleep(delay)
