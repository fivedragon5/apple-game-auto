from typing import List, Tuple

def is_valid_rect(x1, y1, x2, y2, ROWS, COLS):
    return 0 <= x1 <= x2 < ROWS and 0 <= y1 <= y2 < COLS and (x2 - x1 + 1) <= 5 and (y2 - y1 + 1) <= 5

def sum_and_check(grid, x1, y1, x2, y2):
    total = 0
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            if grid[i][j] == -1:
                return -1
            total += grid[i][j]
    return total

def zero_out(grid, x1, y1, x2, y2):
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            grid[i][j] = 0

def count_cells(x1, y1, x2, y2):
    return (x2 - x1 + 1) * (y2 - y1 + 1)

def greedy_sum10_rectangles(grid: List[List[int]]) -> List[Tuple[int, int, int, int]]:
    ROWS, COLS = len(grid), len(grid[0])
    result = []

    while True:
        best = None
        max_cells = 0

        for x1 in range(ROWS):
            for y1 in range(COLS):
                for x2 in range(x1, min(x1 + 5, ROWS)):
                    for y2 in range(y1, min(y1 + 5, COLS)):
                        if not is_valid_rect(x1, y1, x2, y2, ROWS, COLS):
                            continue
                        s = sum_and_check(grid, x1, y1, x2, y2)
                        if s == 10:
                            area = count_cells(x1, y1, x2, y2)
                            if area > max_cells:
                                max_cells = area
                                best = (x1, y1, x2, y2)

        if best is None:
            break  # 더 이상 찾을 수 없음

        x1, y1, x2, y2 = best
        zero_out(grid, x1, y1, x2, y2)
        result.append((y1, x1, y2, x2))  # 반환값 포맷: (x1, y1, x2, y2) → (col,row,col,row)

    return result
