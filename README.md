*This project has been created as part of the 42 curriculum by dcoelho, hede-car.*

# A-Maze-ing

## 1. Description

A-Maze-ing is a Python maze generator and solver. Given a small text
configuration file, it procedurally builds a maze (perfect or imperfect),
solves it with a shortest-path search, writes the result to a hexadecimal
output file, and displays it interactively — either in the terminal or
through an MLX graphical window.

The maze is always built around a hidden **"42"** pattern of fully closed
cells, and the generation logic itself is packaged as a standalone,
reusable Python library (`mazegen`) so it can be imported and reused in
other projects.

## 2. Instructions

### 2.1. Requirements

- Python 3.10+
- MiniLibX (MLX) bindings, used only for the graphical rendering mode
  (bundled under `mazegen/mlx`)

### 2.2. Setup and usage

```bash
make install   # install project dependencies
make run       # runs: python3 a_maze_ing.py config.txt
make debug     # runs the program under pdb
make clean     # removes __pycache__ / .mypy_cache directories
make lint      # flake8 + mypy (standard flags)
make lint-strict  # flake8 + mypy --strict
```

You can also run it directly:

```bash
python3 a_maze_ing.py config.txt
```

`a_maze_ing.py` is the entry point and `config.txt` is the only argument:
a plain text configuration file (you may use a different filename/path).
Any invalid configuration, missing file, bad syntax, or impossible maze
parameters is caught and reported with a clear error message instead of
crashing.

### 2.3. Configuration file format

One `KEY=VALUE` pair per line; lines starting with `#` are ignored.

| Key | Required | Description | Example |
|---|---|---|---|
| `WIDTH` | yes | Maze width, in cells (min. 2) | `WIDTH=15` |
| `HEIGHT` | yes | Maze height, in cells (min. 2) | `HEIGHT=20` |
| `ENTRY` | yes | Entry coordinates `row,col`, inside the maze | `ENTRY=0,0` |
| `EXIT` | yes | Exit coordinates `row,col`, different from entry | `EXIT=19,14` |
| `OUTPUT_FILE` | yes | Path of the generated output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | yes | `True` for a perfect maze (single path entry→exit), `False` to add loops | `PERFECT=True` |
| `SEED` | no | RNG seed, for reproducible mazes (random if omitted) | `SEED=522780` |
| `ALGORITHM` | no | `RecursiveBacktracker` (default), `Prim` or `Kruskal` | `ALGORITHM=Kruskal` |

Example (`config.txt`, provided at the repository root):

```
WIDTH=15
HEIGHT=20
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### 2.4. Output file format

- One hexadecimal digit per cell, cells stored row by row (one row per line).
  Each digit's bits mark which walls are **closed** (1) or **open** (0):
  bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West.
- After a blank line: the entry coordinates, the exit coordinates, and the
  shortest path from entry to exit as a string of `N`/`E`/`S`/`W` letters —
  each on its own line.

### 2.5. Visual representation

The maze is rendered in an MLX window, showing the walls, the entry (green)
and exit (red) cells, the "42" mask, and the shortest solution path.
Available controls (number keys):

| Key | Action |
|---|---|
| `1` | Cycle through the available wall-colour themes (11 themes, e.g. Classic, Neon, Ocean, Forest…) |
| `2` | Regenerate a new maze with a fresh random seed |
| `3` | Show / hide the solution path |
| `4` | Quit |

## 3. Maze generation algorithm

Three generation algorithms are implemented, selectable via the
`ALGORITHM` config key:

- **Recursive Backtracker** (default) — implemented first, as it is the
  simplest depth-first-search-based approach to get a perfect maze working
  end to end.
- **Prim's algorithm** and **Kruskal's algorithm** — added afterwards as a
  bonus, to support several generation styles.

These three were picked specifically because they are the most popular maze generation algorithms, which meant there was the most documentation and explanatory material available to learn how each of them works.

All three produce a perfect (spanning-tree) maze by default; when
`PERFECT=False`, extra walls are randomly removed afterwards to create
loops (an imperfect maze).

## 4. Code reusability

The whole maze generation, solving and rendering logic lives in the `mazegen` package
(`mazegen/`), so it can be
reused in other projects. It is built as a standalone, installable
package (see `mazegen-1.0.0-py3-none-any.whl` at the repository root),
built from `pyproject.toml`.

### 4.1. Basic usage

```python
from mazegen import RecursiveBacktracker, maze_solver

settings = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (14, 19),
    "SEED": 42,          # or None for a random seed
    "PERFECT": True,
    "OUTPUT_FILE": "maze.txt",
}

maze = RecursiveBacktracker(settings)   # or Prim(settings) / Kruskal(settings)
maze.generate_maze()

path = maze_solver(maze)   # shortest path as a string of N/E/S/W letters
```

### 4.2. Custom parameters

Pass a `settings` dict to any of the three generator classes
(`RecursiveBacktracker`, `Prim`, `Kruskal`), all exported by `mazegen`:

- `WIDTH` / `HEIGHT`: size of the maze, in cells
- `ENTRY` / `EXIT`: `(row, col)` tuples
- `SEED`: any value accepted by `random.Random`, or `None` for a random seed
- `PERFECT`: `True`/`False`
- `OUTPUT_FILE`: path used by `maze_solver` to write the maze/solution to

### 4.3. Accessing the generated structure and solution

- `maze.grid` is a `height` x `width` list of `Cell` objects. Each `Cell`
  has `.north` / `.east` / `.south` / `.west` (`1` = wall closed, `0` =
  open) and `.pos` (its `(row, col)` coordinates). Note that this is not
  the same format as the hexadecimal output file — it's the in-memory
  representation.
- `maze_solver(maze)` returns the shortest entry->exit path as a string of
  `N`/`E`/`S`/`W` letters, and also writes the maze, entry/exit coordinates
  and this path to `maze.output_file`.

Building the package again from source:

```bash
pip install build
python3 -m build .
```

## 5. Team and project management

- **dcoelho**: visual representation (MLX renderer), the maze solver
  (shortest path), and the `Cell` class.
- **hede-car**: the Prim and Kruskal maze generation algorithms, and the colour
  schemes used in the maze rendering.
- **Both**: the configuration file parsing, Recursive Backtracker generation algorithm plus ongoing peer discussion and
  contributions to each other's parts.

The initial task breakdown was established without full upfront planning: the main tasks were identified and divided between the two team members, and any newly identified tasks or problems were picked up by whoever had less on their plate at the time. This division of work proved effective, as ongoing mutual support and discussion helped resolve issues along the way. One area for improvement would have been more upfront planning — in particular, deciding which bonuses to pursue from the start, rather than only considering them after the mandatory part was completed. Specific requirements and implementation approaches were also discussed with other peers working on, or who had already completed, the same project.

## 6. Resources

- [Wikipedia — Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Jamis Buck — Buckblog, "Maze Generation" series](https://weblog.jamisbuck.org/archives.html) (Recursive Backtracker, Prim's and Kruskal's algorithms explained and animated)
- 42's MiniLibX documentation

**AI usage**: AI (Claude) was used to help clarify how the maze generation
algorithms and MiniLibX (MLX) work, in addition to the well-known
references above, and to help generate some of the colour schemes used in
the maze rendering. It was also used afterwards to add docstrings to the
codebase's and to do the README structure.
