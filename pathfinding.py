from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

Pos = Tuple[int, int] # (row, col)
Grid = List[List[str]]


EXAMPLE_MAP_1 = """
##########
#S..#....#
#..##.##.#
#...#...G#
##########
""".strip("\n")

EXAMPLE_MAP_2 = """
############
#S.....#...#
###.##.#.#.#
#...#..#.#G#
#.###..#...#
#......###.#
############
""".strip("\n")


def parse_grid(text: str) -> Tuple[Grid, Pos, Pos]:
    """
    Convert a multiline string map into a grid plus start and goal positions.

    Map legend:
    '#' wall
    '.' floor
    'S' start (exactly one)
    'G' goal (exactly one)
    """
    raise NotImplementedError


def neighbors(grid: Grid, node: Pos) -> List[Pos]:
    """Return valid 4-direction neighbors that are not walls."""
    raise NotImplementedError


def reconstruct_path(parent: Dict[Pos, Pos], start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """Reconstruct path from start->goal using parent pointers. Return None if goal unreachable."""
    raise NotImplementedError


def bfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Queue-based BFS.
    Return (path, visited).
    - path is a list of positions from start to goal (inclusive), or None.
    - visited contains all explored/seen nodes.
    """
    raise NotImplementedError


def dfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Stack-based DFS (iterative, no recursion).
    Return (path, visited).
    """
    raise NotImplementedError


def render(grid: Grid, path: Optional[List[Pos]] = None, visited: Optional[Set[Pos]] = None) -> str:
    """
    Render the grid as text.
    Overlay rules (recommended):
    - path tiles shown as '*'
    - visited tiles shown as '·' (middle dot) or '+'
    - preserve 'S' and 'G'
    """
    raise NotImplementedError


def run_one(label: str, grid_text: str) -> None:
    grid, start, goal = parse_grid(grid_text)

print("=" * 60)
print(label)
print("- Raw map")
print(render(grid))

path_bfs, visited_bfs = bfs_path(grid, start, goal)
print("\n- BFS")
print(f"found={path_bfs is not None} path_len={(len(path_bfs) if path_bfs else None)} visited={len(visited_bfs)}")
print(render(grid, path=path_bfs, visited=visited_bfs))

path_dfs, visited_dfs = dfs_path(grid, start, goal)
print("\n- DFS")
print(f"found={path_dfs is not None} path_len={(len(path_dfs) if path_dfs else None)} visited={len(visited_dfs)}")
print(render(grid, path=path_dfs, visited=visited_dfs))


def main() -> None:
   run_one("Example Map 1", EXAMPLE_MAP_1)
   run_one("Example Map 2", EXAMPLE_MAP_2)


if __name__ == "__main__": main()
