from config import SCREENSHOT_TAKE_DELAY
from datetime import datetime
from screenshot import take_screenshot
from ocr import check_image
from recognize import greedy_sum10_rectangles
from mouse import drag_all
import time
import sys

print("=== 사과 게임 시작 ===")

# 현재 시간 파일명 생성
fileName = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# 사진 찍기전 딜레이 시간
time.sleep(SCREENSHOT_TAKE_DELAY)

# 스크린샷 찍기
take_screenshot(fileName)

# 이미지 문자 추출
grid = check_image(fileName)

# 경로 탐색 시작
result = greedy_sum10_rectangles(grid)

for coords in result:
    print(coords)

# 드래그 수행
drag_all(result)

print("=== 사과 게임 종료 ===")
sys.exit(0)
