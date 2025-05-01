import os

# 이미지 파일 경로 설정
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
IMAGE_SCREENSHOT_FOLDER = ROOT_DIR + "/image/screenshot/" # 스크린샷 폴더
IMAGE_CONVERT_FOLDER = ROOT_DIR + "/image/convert/" # 변환된 이미지 폴더
IMAGE_DEBUG_FOLDER = ROOT_DIR + "/image/debug_cells/" # 디버그 셀 이미지 폴더

# 폴더가 없을 경우 설정
os.makedirs(IMAGE_SCREENSHOT_FOLDER, exist_ok=True)
os.makedirs(IMAGE_CONVERT_FOLDER, exist_ok=True)
os.makedirs(IMAGE_DEBUG_FOLDER, exist_ok=True)

# SCREENSHOT 설정
SCREENSHOT_OFFSET_X = 435   # 스크린샷 시작 X 좌표
SCREENSHOT_OFFSET_Y = 280   # 스크린샷 시작 Y 좌표
SCREENSHOT_WIDTH = 1000     # 스크린샷 너비
SCREENSHOT_HEIGHT = 585     # 스크린샷 높이
SCREENSHOT_TAKE_DELAY = 5   # 스크린샷 찍기 전 대기 시간

# OCR 설정
PYTESSERACT_CMD = '/opt/homebrew/bin/tesseract' # Tesseract 설치 경로

# DRAG 설정
DRAG_OFFSET_X = 445                 # 드래그 시작 X 좌표
DRAG_OFFSET_Y = 285                 # 드래그 시작 Y 좌표
DRAG_CELL_WIDTH = 56                # 드래그 셀 너비
DRAG_CELL_HEIGHT = 56               # 드래그 셀 높이
DRAG_MOUSE_DOWN_DELAY = 0.02        # 마우스 다운 대기 시간
DRAG_MOUSE_MOVE_TO_DURATION = 0.1  # 마우스 드래그 이동 시간
