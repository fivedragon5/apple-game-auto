from config import DRAG_OFFSET_X, DRAG_OFFSET_Y, DRAG_CELL_WIDTH, DRAG_CELL_HEIGHT, DRAG_MOUSE_DOWN_DELAY, DRAG_MOUSE_MOVE_TO_DURATION
from pynput import keyboard
import pyautogui
import time

# 셀 좌표 계산 함수들
def get_top_left(col, row):
    offset_x, offset_y = DRAG_OFFSET_X, DRAG_OFFSET_Y
    cell_width, cell_height = DRAG_CELL_WIDTH, DRAG_CELL_HEIGHT
    return offset_x + col * cell_width, offset_y + row * cell_height

def get_bottom_right(col, row):
    offset_x, offset_y = DRAG_OFFSET_X, DRAG_OFFSET_Y
    cell_width, cell_height = DRAG_CELL_WIDTH, DRAG_CELL_HEIGHT
    return offset_x + (col + 1) * cell_width, offset_y + (row + 1) * cell_height

# 드래그 함수
def drag_one(x1, y1, x2, y2):
    start_x, start_y = get_top_left(x1, y1)
    end_x, end_y = get_bottom_right(x2, y2)
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    time.sleep(DRAG_MOUSE_DOWN_DELAY)
    pyautogui.moveTo(end_x, end_y, duration=DRAG_MOUSE_MOVE_TO_DURATION)
    pyautogui.mouseUp()

# 상태 변수
cancelled = False

# 키보드 리스너 콜백
def on_press(key):
    global cancelled
    try:
        if key.char == 'q':
            cancelled = True
            print("\n'q' 키가 눌렸습니다. 드래그 취소 중...")
            return False  # 리스너 종료
    except AttributeError:
        pass

def drag_all(result):
    global cancelled
    cancelled = False
    print("드래그 시작... 'q' 키를 누르면 종료 됩니다.")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    for i, (x1, y1, x2, y2) in enumerate(result):
        if cancelled:
            print(f"\n드래그 중 취소됨 (현재 {i+1}/{len(result)} 완료)")
            break
        drag_one(x1, y1, x2, y2)

if __name__ == "__main__":
    sample_result = [[0, 0, 1, 0], [1, 1, 2, 1], [0, 2, 2, 0]]
    drag_all(sample_result)
