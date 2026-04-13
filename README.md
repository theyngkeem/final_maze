*This project has been created as part of the 42 curriculum by yaarab, otkibou.*
 
# A_maze_ing
 
## Description
 
A_maze_ing is a Python application that generates and displays mazes. Users can configure the maze dimensions, entry/exit points, generation algorithm, and whether the maze is "perfect" (single solution) or "imperfect" (multiple paths). The result can be visualized in a window and saved as a text file.
 
---
 
## Instructions
 
### Prerequisites
 
- Python 3
- `pip`
 
### Installation
 
```bash
make install
```
 
### Execution
 
```bash
python3 a_maze_ing.py config.txt
# or
make run
```
 
### Configuration File
 
The maze is configured via a key-value text file with the following structure:
 
| Key | Type | Description |
|-----|------|-------------|
| `WIDTH` | integer | Number of columns in the maze |
| `HEIGHT` | integer | Number of rows in the maze |
| `ENTRY` | x,y | Entry point coordinates (column, row) |
| `EXIT` | x,y | Exit point coordinates (column, row) |
| `OUTPUT_FILE` | filename | Path to save the maze as a `.txt` file |
| `PERFECT` | true/false | `true` = no loops, single solution; `false` = may have loops |
| `SEED` | integer or empty | RNG seed for reproducible mazes; leave blank for random |
 
**Example `config.txt`:**
```
WIDTH=20
HEIGHT=10
ENTRY=0,0
EXIT=19,9
OUTPUT_FILE=maze.txt
PERFECT=true
SEED=42
```
 
---
 
## Maze Generation
 
### Algorithms
 
**DFS — Depth-First Search** *(used for generation)*
Carves passages by exploring as far as possible in one direction before backtracking. This naturally produces long, winding corridors and guarantees a single path between any two cells — making it a perfect fit for generating "perfect" mazes. For imperfect mazes, extra walls are removed afterward to create loops.
 
**Why DFS?**
DFS is simple to implement, memory-efficient with a stack, and reliably produces mazes with a good balance of complexity and solvability. It maps directly to the definition of a perfect maze, which was a core requirement of the project.
 
**BFS — Breadth-First Search** *(used for solving)*
Explores all neighbors level by level. Used to find and animate the shortest path from entry to exit after the maze is generated.
 
### Perfect vs Imperfect
 
- **Perfect** (`PERFECT=true`): Every cell is reachable and there is exactly **one** path between any two points — no loops.
- **Imperfect** (`PERFECT=false`): Extra passages are carved into the perfect maze, creating loops and **multiple possible routes**.
 
---
 
## Bonus
 
Path animation — once the maze is generated, BFS finds the shortest solution and the path is animated step by step in the display window.
 
---
 
## MazeGenerator — Reusable Module

### Install in a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install --upgrade pip build
pip install mazegen-1.0.0-py3-none-any.whl
```

To rebuild the package from source:

```bash
python3 -m build                # produces .whl and .tar.gz in dist/
```

---

### Usage

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=20,           # number of columns
    height=10,          # number of rows
    entry=(0, 0),       # (col, row) of the entry point
    exit_=(19, 9),      # (col, row) of the exit point
    perfect=True,       # True = single solution, False = multiple paths
    seed=42             # optional: integer for reproducible results, None for random
)

gen.generate()
```

### Accessing the maze structure

The maze is exposed as `gen.table`, a 2D list of integers where each value is a bitmask encoding which walls are **present** on that cell:

| Constant | Value | Wall |
|----------|-------|------|
| `NORTH`  | 1     | top  |
| `EAST`   | 2     | right |
| `SOUTH`  | 4     | bottom |
| `WEST`   | 8     | left |

```python
cell = gen.table[row][col]   # integer bitmask
```

### Accessing the solution

After `generate()`, the solution is available as `gen.path` — a string of direction characters (`N`, `S`, `E`, `W`) leading from entry to exit:

```python
print(gen.path)   # e.g. "EESSSEEN..."
```
 
---
 
## Team & Project Management
 
### Roles
 
| Member | Responsibilities |
|--------|-----------------|
| yaarab | DFS & BFS algorithms, config parser, file output |
| otkibou | Display (terminal rendering) |
 
### Planning & Evolution
 
The initial plan was to build in this order: core generation → config parsing → integration → output/display → polish. This was largely followed:
 
1. **Core logic** — `MazeGenerator` class with DFS algorithm
2. **Configuration** — `config_parser.py` for flexible setup
3. **Integration** — wiring parser to generator in `a_maze_ing.py`
4. **Output** — `write_output.py` and `display.py` for results
5. **Bonus** — BFS path solving and step-by-step animation
 
The main deviation was that error handling in the parser was added later than planned, which caused some friction during integration.
 
### What Worked Well & What Could Be Improved
 
**Worked well:** The modular structure made it easy to develop and debug each component independently. Clear separation of concerns (generation, display, output) meant both team members could work in parallel without conflicts.
 
**Could be improved:** A `requirements.txt` should have been set up from day one. Error handling in the config parser was added reactively rather than planned upfront, which slowed down the integration phase.
 
### Tools Used
 
- **Editor:** VS Code
- **Linting:** `flake8` (style), `mypy` (type checking)
- **Debugging:** `pdb` via `make debug`
- **Version Control:** Git
 
---
 
## Resources
 
### References
 
- [Maze Generation Algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — Overview of various maze generation strategies
- [Depth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search) — Core algorithm used for maze generation
- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search) — Algorithm used for pathfinding/animation
 
### AI Usage
 
GitHub Copilot was used for:
- **Docstrings & comments** — documentation for functions and classes
- **Debugging assistance** — suggesting fixes for mypy errors
- **README structuring** — helping organize this file based on project requirements
 