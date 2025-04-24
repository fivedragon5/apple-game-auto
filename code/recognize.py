import pytesseract
import cv2
import numpy as np

from screenshot import load_screenshot

def check_image(image_name):
    failCount = 0

    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
    # 기본 설정
    ROWS, COLS = 10, 17

    # 이미지 로드
    image = load_screenshot(image_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("./debug_cells/" + image_name + "_gray.png", gray)

    # 색상 반전
    inverted = cv2.bitwise_not(gray)
    cv2.imwrite("./debug_cells/" + image_name + "inverted.png", inverted)

    # 이진화
    _, binaryFullImage = cv2.threshold(inverted, 100, 255, cv2.THRESH_BINARY)
    cv2.imwrite("./debug_cells/" + image_name + "binary.png", binaryFullImage)

    height, width = binaryFullImage.shape
    cell_h = height // ROWS
    cell_w = width // COLS

    # ====== 결과 그리드 초기화 ======
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

    # ====== 셀 단위로 잘라서 OCR 수행 ======
    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * cell_w
            y1 = row * cell_h
            cell_img = binaryFullImage[y1:y1 + cell_h, x1:x1 + cell_w]

            resized = cv2.resize(cell_img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

            # OCR (숫자만 허용)
            config = "--psm 10 -c tessedit_char_whitelist=123456789"
            text = pytesseract.image_to_string(resized, config=config).strip()

            # 재시도 전처리 (OCR 실패 셀만)
            if not text.isdigit():
                print(f"[{row}, {col}] retry")
                reResized = cv2.resize(cell_img, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
                kernel = np.ones((2, 2), np.uint8)
                dilated = cv2.dilate(reResized, kernel, iterations=1) # 팽창
                cleaned = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=2)

                config_alt = "--psm 8 -c tessedit_char_whitelist=123456789"
                text_retry = pytesseract.image_to_string(cleaned, config=config_alt).strip()

                if text_retry.isdigit():
                    text = text_retry
                    grid[row][col] = text
                else:
                    print("실패")
                    failCount += 1
                    grid[row][col] = -1

            grid[row][col] = text

            # 디버깅용 이미지 저장
            cell_filename = f"./debug_cells/cell_{row}_{col}_{text if text else 'empty'}.png"
            cv2.imwrite(cell_filename, resized)

    # ====== 결과 출력 ======
    print("Total Fail Count:", failCount)
    for row in grid:
        print(" ".join(cell.rjust(2) if cell else ' .' for cell in row))

    return grid