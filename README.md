# BFS + DFS Pathfinding (Python Console)

## Run
```bash
python pathfinding.py
```

The script now has two parts:
- BFS/DFS demos on built-in `S` → `G` maps that print found/path length/visited and rendered overlays.
- A simple turn-based **Monster Chase** game (interactive terminals only).

## Monster Chase
- Map legend: `P` player, `M` monster, `#` wall, `.` floor, optional `G` exit.
- Move with `W/A/S/D` (`q` to quit).
- Monster recomputes a path to the player every turn and moves one step.
- Set `MODE = "BFS"` or `MODE = "DFS"` in `pathfinding.py` to choose monster behavior.
- Lose if monster reaches player; win if player reaches `G`.
