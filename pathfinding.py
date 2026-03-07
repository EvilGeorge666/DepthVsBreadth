from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

Pos = Tuple[int, int]  # (row, col)
Grid = List[List[str]]

MODE = "BFS"  # Change to "DFS" for DFS-driven monster pathing.


EXAMPLE_MAP_1 = """
##########
#S.......#
#.######.#
#.......G#
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

GAME_MAP = """
############
#P...#.....#
#.##.#.###.#
#....#...#.#
#.####.#.#.#
#....#.#...#
#.##.#.###.#
#..G....#M.#
############
""".strip("\n")


@dataclass
class GameState:
    grid: Grid
    player: Pos
    monster: Pos
    goal: Optional[Pos]


def parse_grid(text: str) -> Tuple[Grid, Pos, Pos]:
    """
    Convert a multiline string map into a grid plus start and goal positions.

    Map legend:
    '#' wall
    '.' floor
    'S' start (exactly one)
    'G' goal (exactly one)
    """
    lines = [list(line) for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Map is empty")

    width = len(lines[0])
    for row in lines:
        if len(row) != width:
            raise ValueError("Map rows must all have same width")

    start: Optional[Pos] = None
    goal: Optional[Pos] = None
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "S":
                if start is not None:
                    raise ValueError("Map must contain exactly one S")
                start = (r, c)
            elif ch == "G":
                if goal is not None:
                    raise ValueError("Map must contain exactly one G")
                goal = (r, c)

    if start is None or goal is None:
        raise ValueError("Map must contain one S and one G")

    return lines, start, goal


def neighbors(grid: Grid, node: Pos) -> List[Pos]:
    """Return valid 4-direction neighbors that are not walls."""
    r, c = node
    out: List[Pos] = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
            out.append((nr, nc))
    return out


def reconstruct_path(parent: Dict[Pos, Pos], start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """Reconstruct path from start->goal using parent pointers. Return None if goal unreachable."""
    if goal != start and goal not in parent:
        return None

    path = [goal]
    cur = goal
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def bfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Queue-based BFS.
    Return (path, visited).
    - path is a list of positions from start to goal (inclusive), or None.
    - visited contains all explored/seen nodes.
    """
    q: deque[Pos] = deque([start])
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while q:
        cur = q.popleft()
        if cur == goal:
            return reconstruct_path(parent, start, goal), visited

        for nxt in neighbors(grid, cur):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                q.append(nxt)

    return None, visited


def dfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Stack-based DFS (iterative, no recursion).
    Return (path, visited).
    """
    stack: List[Pos] = [start]
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while stack:
        cur = stack.pop()
        if cur == goal:
            return reconstruct_path(parent, start, goal), visited

        for nxt in reversed(neighbors(grid, cur)):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                stack.append(nxt)

    return None, visited


def render(grid: Grid, path: Optional[List[Pos]] = None, visited: Optional[Set[Pos]] = None) -> str:
    """
    Render the grid as text.
    Overlay rules (recommended):
    - path tiles shown as '*'
    - visited tiles shown as '·' (middle dot) or '+'
    - preserve 'S' and 'G'
    """
    canvas = [row[:] for row in grid]

    if visited:
        for r, c in visited:
            if canvas[r][c] not in {"S", "G", "#"}:
                canvas[r][c] = "+"

    if path:
        for r, c in path:
            if canvas[r][c] not in {"S", "G", "#"}:
                canvas[r][c] = "*"

    return "\n".join("".join(row) for row in canvas)


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


def parse_game_grid(text: str) -> GameState:
    lines = [list(line) for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Game map is empty")

    width = len(lines[0])
    for row in lines:
        if len(row) != width:
            raise ValueError("Game map rows must all have same width")

    player: Optional[Pos] = None
    monster: Optional[Pos] = None
    goal: Optional[Pos] = None

    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "P":
                if player is not None:
                    raise ValueError("Game map must contain exactly one P")
                player = (r, c)
                lines[r][c] = "."
            elif ch == "M":
                if monster is not None:
                    raise ValueError("Game map must contain exactly one M")
                monster = (r, c)
                lines[r][c] = "."
            elif ch == "G":
                if goal is not None:
                    raise ValueError("Game map can contain at most one G")
                goal = (r, c)

    if player is None or monster is None:
        raise ValueError("Game map must contain P and M")

    return GameState(grid=lines, player=player, monster=monster, goal=goal)


def render_game(state: GameState) -> str:
    canvas = [row[:] for row in state.grid]
    if state.goal is not None:
        gr, gc = state.goal
        canvas[gr][gc] = "G"

    pr, pc = state.player
    mr, mc = state.monster
    canvas[pr][pc] = "P"
    canvas[mr][mc] = "M"
    return "\n".join("".join(row) for row in canvas)


def player_step(state: GameState, move: str) -> None:
    deltas = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
    }
    if move not in deltas:
        return

    dr, dc = deltas[move]
    nr, nc = state.player[0] + dr, state.player[1] + dc
    if 0 <= nr < len(state.grid) and 0 <= nc < len(state.grid[0]) and state.grid[nr][nc] != "#":
        state.player = (nr, nc)


def monster_step(state: GameState, mode: str) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    mode = mode.upper()
    if mode == "DFS":
        path, visited = dfs_path(state.grid, state.monster, state.player)
    else:
        path, visited = bfs_path(state.grid, state.monster, state.player)

    if path and len(path) > 1:
        state.monster = path[1]
    return path, visited


def play_game(mode: str = MODE) -> None:
    state = parse_game_grid(GAME_MAP)
    mode = mode.upper()

    print("\n" + "=" * 60)
    print(f"Monster Chase ({mode})")
    print("Controls: W/A/S/D to move, q to quit.")

    while True:
        print("\n" + render_game(state))
        move = input("Your move: ").strip().lower()
        if move == "q":
            print("Game ended.")
            return

        player_step(state, move)
        if state.player == state.monster:
            print("The monster caught you. You lose!")
            print(render_game(state))
            return

        if state.goal is not None and state.player == state.goal:
            print("You reached the exit. You win!")
            print(render_game(state))
            return

        path, visited = monster_step(state, mode)
        print(f"Monster searched with {mode}: found={path is not None}, path_len={(len(path) if path else None)}, visited={len(visited)}")

        if state.player == state.monster:
            print("The monster caught you. You lose!")
            print(render_game(state))
            return


def main() -> None:
    run_one("Example Map 1", EXAMPLE_MAP_1)
    run_one("Example Map 2", EXAMPLE_MAP_2)

    if sys.stdin.isatty():
        play_game(MODE)
    else:
        print("\nSkipping Monster Chase game (non-interactive stdin).")


if __name__ == "__main__":
    main()
