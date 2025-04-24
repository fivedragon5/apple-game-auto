import tkinter as tk
import pyautogui
import time

# 설정 값 (GUI에서 변경 가능하도록 위젯으로 만들 수도 있습니다.)
OFFSET_X, OFFSET_Y = 450, 290
CELL_WIDTH, CELL_HEIGHT = 57, 57
DRAG_DELAY = 0.5  # 드래그 사이의 딜레이 (초)

# 셀 하나의 좌측 상단 좌표 계산 함수
def get_top_left(col, row):
    x = OFFSET_X + col * CELL_WIDTH
    y = OFFSET_Y + row * CELL_HEIGHT
    return x, y

# 셀 하나의 우측 하단 좌표 계산 함수
def get_bottom_right(col, row):
    x = OFFSET_X + (col + 1) * CELL_WIDTH
    y = OFFSET_Y + (row + 1) * CELL_HEIGHT
    return x, y

# 드래그 한번 수행 (pyautogui 사용)
def drag_one_pyautogui(x1, y1, x2, y2):
    start_x, start_y = get_top_left(x1, y1)
    end_x, end_y = get_bottom_right(x2, y2)

    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    time.sleep(0.05)
    pyautogui.moveTo(end_x, end_y, duration=0.15)
    pyautogui.mouseUp()

# 전체 드래그 실행 (pyautogui 사용)
def execute_drag_all(result):
    for x1, y1, x2, y2 in result:
        drag_one_pyautogui(x1, y1, x2, y2)
        time.sleep(DRAG_DELAY)

# 버튼 클릭 이벤트 핸들러
def start_drag():
    # 예시 드래그 경로 (실제 경로는 알고리즘 결과에 따라 달라집니다.)
    drag_paths = [(0, 0, 2, 0), (1, 0, 1, 1)]
    execute_drag_all(drag_paths)
    status_label.config(text="드래그 완료")

# GUI 창 생성
window = tk.Tk()
window.title("자동 드래그")

# 상태 레이블
status_label = tk.Label(window, text="준비")
status_label.pack(pady=10)

# 드래그 시작 버튼
drag_button = tk.Button(window, text="드래그 시작", command=start_drag)
drag_button.pack(pady=20)

# GUI 실행
window.mainloop()