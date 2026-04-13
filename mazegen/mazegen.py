from typing import Optional
import random
from collections import deque


NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

OPPOSITE: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

MOVES: dict[int, tuple[int, int]] = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    EAST: (0, 1),
    WEST: (0, -1),
}


PATTERN_42 = [
    [1, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 1, 1],
]


class MazeGenerator:
    """generating the maze"""
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit_: tuple[int, int], perfect: bool,
                 seed: Optional[int | str],):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.perfect = perfect
        self.seed: Optional[int | str | float] = seed
        self.rnd = random.Random(seed)
        self.table = [[15 for _ in range(width)] for _ in range(height)]
        self.path = ""
        self.logo_cells: set[tuple[int, int]] = set()

    def _forty_two_cells(self) -> set[tuple[int, int]]:
        if self.height < 9 or self.width < 13:
            return set()
        offset_row = (self.height - 5) // 2
        offset_col = (self.width - 9) // 2

        coords: set[tuple[int, int]] = set()
        for row in range(5):
            for col in range(9):
                if PATTERN_42[row][col] == 1:
                    coords.add((offset_col + col, offset_row + row))
        return coords

    def get_dir(self, row: int, col: int,
                visited: list[list[bool]]) -> list[tuple[int, int, int]]:
        """decide where to go based on visited cells"""
        res = []
        directions = [NORTH, EAST, SOUTH, WEST]
        for d in directions:
            dr, dc = MOVES[d]
            nrow, ncol = row + dr, col + dc
            if self.check_pos(nrow, ncol) and not visited[nrow][ncol]:
                res.append((d, nrow, ncol))
        return res

    def remove_wall(self, row: int, col: int, direction: int) -> None:
        """remove wall while tracing the maze"""
        self.table[row][col] &= ~direction
        dr, dc = MOVES[direction]
        nrow, ncol = row + dr, col + dc
        self.table[nrow][ncol] &= ~OPPOSITE[direction]

    def check_pos(self, row: int, col: int) -> bool:
        """check if next position inside the maze"""
        if not (0 <= row < self.height and 0 <= col < self.width):
            return False
        return True

    def _dfs(self, start_row: int, start_col: int,
             visited: list[list[bool]]) -> None:
        visited[start_row][start_col] = True
        stack = [(start_row, start_col)]
        while stack:
            row, col = stack[-1]
            nbr = self.get_dir(row, col, visited)
            if nbr:
                direction, nrow, ncol = self.rnd.choice(nbr)
                self.remove_wall(row, col, direction)
                visited[nrow][ncol] = True
                stack.append((nrow, ncol))
            else:
                stack.pop()

    def dfs(self) -> None:
        visited = [[False for _ in range(self.width)]
                   for _ in range(self.height)]
        for col, row in self.logo_cells:
            if self.check_pos(row, col):
                visited[row][col] = True
        scol, srow = self.entry
        if self.check_pos(srow, scol) and not visited[srow][scol]:
            self._dfs(srow, scol, visited)
        for row in range(self.height):
            for col in range(self.width):
                if visited[row][col]:
                    continue
                self._dfs(row, col, visited)

    def hawtha(self) -> None:
        for row in range(self.height):
            self.table[row][0] |= WEST
            self.table[row][self.width - 1] |= EAST

        for col in range(self.width):
            self.table[0][col] |= NORTH
            self.table[self.height - 1][col] |= SOUTH

    def bfs(self) -> str:
        visited = [[False for _ in range(self.width)]
                   for _ in range(self.height)]
        scol, srow = self.entry
        visited[srow][scol] = True
        path = deque([(srow, scol, "")])
        directions = {NORTH: "N", EAST: "E", SOUTH: "S", WEST: "W"}
        while path:
            row, col, sol = path.popleft()
            if (col, row) == self.exit_:
                return sol
            for d in directions.keys():
                if self.table[row][col] & d == 0:
                    nr, nc = MOVES[d]
                    nrow, ncol = row + nr, col + nc
                    if self.check_pos(nrow, ncol) and not visited[nrow][ncol]:
                        visited[nrow][ncol] = True
                        path.append((nrow, ncol, sol + directions[d]))
        return ""

    def use_sign(self) -> None:
        ecol, erow = self.entry
        xcol, xrow = self.exit_
        if not self.logo_cells:
            print("that a error the maze is too small")
            return

        if (ecol, erow) in self.logo_cells or (xcol, xrow) in self.logo_cells:
            raise ValueError("WARNING the 42 pattern overlap entry or exit")

        for col, row in self.logo_cells:
            if not self.check_pos(row, col):
                continue
            self.table[row][col] = 0xF

        for col, row in self.logo_cells:
            if not self.check_pos(row, col):
                continue
            if self.check_pos(row - 1, col):
                self.table[row - 1][col] |= SOUTH
            if self.check_pos(row + 1, col):
                self.table[row + 1][col] |= NORTH
            if self.check_pos(row, col - 1):
                self.table[row][col - 1] |= EAST
            if self.check_pos(row, col + 1):
                self.table[row][col + 1] |= WEST

    def fix_open_area(self) -> None:
        """the subject require no 3x3 open area"""
        flag = True
        while flag:
            flag = False
            for row in range(self.height - 2):
                for col in range(self.width - 2):
                    if self.open_block(row, col):
                        self.table[row + 1][col + 1] |= SOUTH
                        self.table[row + 2][col + 1] |= NORTH
                        flag = True

    def open_block(self, row: int, col: int) -> bool:
        """Helper func to check open blocks"""
        for r in range(3):
            for c in range(2):
                if self.table[row + r][col + c] & EAST != 0:
                    return False
        for r in range(2):
            for c in range(3):
                if self.table[row + r][col + c] & SOUTH != 0:
                    return False
        return True

    def make_imperfect(self) -> None:
        """make the maze not perfect"""
        candidates = []
        for row in range(self.height):
            for col in range(self.width):
                if (col, row) in self.logo_cells:
                    continue
                for d, (dr, dc) in MOVES.items():
                    if d not in (EAST, SOUTH):
                        continue
                    if not self.check_pos(row + dr, col + dc):
                        continue
                    if (col + dc, row + dr) in self.logo_cells:
                        continue
                    if self.table[row][col] & d:
                        candidates.append((row, col, d))
        if not candidates:
            return
        removed = False
        for row, col, d in candidates:
            if self.rnd.randint(0, 9) == 0:
                self.remove_wall(row, col, d)
                removed = True
        if not removed:
            row, col, d = candidates[0]
            self.remove_wall(row, col, d)

    def generate(self, seed: Optional[int | str | float | None] = 0) -> None:
        if seed:
            self.seed = seed
        self.rnd.seed(self.seed)
        self.table = [[15 for _ in range(self.width)]
                      for _ in range(self.height)]
        self.path = ""
        self.logo_cells = self._forty_two_cells()
        self.dfs()
        if not self.perfect:
            self.make_imperfect()
        self.hawtha()
        self.use_sign()
        self.fix_open_area()
        self.path = self.bfs()
