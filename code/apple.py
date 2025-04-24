from typing import List

DIRECTIONS = [
    (0, 1),   # →
    (1, 0),   # ↓
    (1, 1),   # ↘
    (-1, 1),  # ↗
]

def is_valid(x, y, ROWS, COLS):
    return 0 <= x < ROWS and 0 <= y < COLS

def find_sum10_drag_paths(grid: List[List[int]]) -> List[List[int]]:
    ROWS, COLS = len(grid), len(grid[0])
    result = []

    for x in range(ROWS):
        for y in range(COLS):
            if grid[x][y] == -1:
                continue

            for dx, dy in DIRECTIONS:
                path = []
                sum_val = 0
                cx, cy = x, y

                for _ in range(10):
                    if not is_valid(cx, cy, ROWS, COLS):
                        break
                    if grid[cx][cy] == -1:
                        break

                    path.append((cx, cy))
                    sum_val += grid[cx][cy]

                    if sum_val == 10:
                        x1, y1 = path[0][1], path[0][0]
                        x2, y2 = path[-1][1], path[-1][0]
                        result.append([x1, y1, x2, y2])

                        for px, py in path:
                            grid[px][py] = 0
                        break
                    elif sum_val > 10:
                        break

                    cx += dx
                    cy += dy

    return result
