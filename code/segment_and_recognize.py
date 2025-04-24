import pytesseract
import cv2
import os
import numpy as np

# 스크린샷 로드 함수
def load_screenshot(filename):
    image = cv2.imread(filename)
    if image is None:
        raise FileNotFoundError(f"Image file '{filename}' not found.")
    return image

# OCR 설정 (한글로 되어 있다면 lang 옵션 조정)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# 사과 게임 스크린샷 로드
image = cv2.imread("../image/2025_04_23_16_08_03.png")

# 그레이스케일 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("../image/2025_04_23_16_08_03_1.png", gray)

# 2단계 이진화
# _, binaryFullImage = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
_, binaryFullImage = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
cv2.imwrite("../image/2025_04_23_16_08_03_2.png", binaryFullImage)

# ====== 전체 이미지 팽창 연산 ======
# kernel = np.ones((3, 3), np.uint8)
# dilatedFullImage = cv2.dilate(binaryFullImage, kernel, iterations=1)
# cv2.imwrite("../image/2025_04_23_16_08_03_3.png", dilatedFullImage)

# 기본 설정
ROWS, COLS = 10, 17

height, width = binaryFullImage.shape
cell_h = height // ROWS
cell_w = width // COLS

# ====== 디버그 디렉토리 생성 ======
os.makedirs("./debug_cells", exist_ok=True)

# ====== 결과 그리드 초기화 ======
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# ====== 셀 단위로 잘라서 OCR 수행 ======
for row in range(ROWS):
    for col in range(COLS):
        x1 = col * cell_w
        y1 = row * cell_h
        cell_img = binaryFullImage[y1:y1 + cell_h, x1:x1 + cell_w]

        resized = cv2.resize(cell_img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        _, binaryCellImage = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY)
        # _, binaryCellImage = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY_INV)

        # 팽창 연산 적용
        kernel = np.ones((3, 3), np.uint8)
        openedCellImage = cv2.morphologyEx(binaryCellImage, cv2.MORPH_OPEN, kernel, iterations=1)

        # OCR (숫자만 허용)
        config = "--psm 10 -c tessedit_char_whitelist=123456789"
        text = pytesseract.image_to_string(openedCellImage, config=config).strip()
        # text = pytesseract.image_to_string(binaryCellImage, config=config).strip()

        # 결과 저장
        grid[row][col] = text if text.isdigit() else ""

        # 디버깅용 이미지 저장
        cell_filename = f"../image/cell_{row}_{col}_{text if text else 'empty'}.png"
        cv2.imwrite(cell_filename, binaryCellImage)

# ====== 결과 출력 ======
for row in grid:
    print(" ".join(cell.rjust(2) if cell else ' .' for cell in row))

