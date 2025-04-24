from datetime import datetime
from screenshot import take_screenshot
from check2 import check_image
from apple2 import greedy_sum10_rectangles
from mouse import drag_all

import time

# 기본 값
offset_x, offset_y, width, height = 435, 280, 1000, 585
# 스크린샷 지연 시간
screenshot_delay = 2
# 현재 시간
now = datetime.now()
fileName = now.strftime("%Y_%m_%d_%H_%M_%S")

time.sleep(screenshot_delay)

# 스크린샷 찍기
take_screenshot(fileName, offset_x, offset_y, width, height)

# 이미지 문자 추출
grid = check_image(fileName)

# 경로 탐색 시작
result = greedy_sum10_rectangles(grid)

for coords in result:
    print(coords)

# 드래그 수행
drag_all(result, delay=0.1)
