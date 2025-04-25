from config import IMAGE_SCREENSHOT_FOLDER, IMAGE_CONVERT_FOLDER, IMAGE_DEBUG_FOLDER, PYTESSERACT_CMD
import pytesseract
import cv2
import numpy as np

def check_image(image_name):
    # OCR 설정
    pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_CMD

    # 사과 게임 스크린샷 로드
    image = cv2.imread(IMAGE_SCREENSHOT_FOLDER + image_name + ".png")

    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(IMAGE_CONVERT_FOLDER + image_name + "_gray.png", gray)

    # 색상 반전
    inverted = cv2.bitwise_not(gray)
    cv2.imwrite(IMAGE_CONVERT_FOLDER + image_name + "_inverted.png", inverted)

    # 이진화
    _, binaryFullImage = cv2.threshold(inverted, 100, 255, cv2.THRESH_BINARY)
    cv2.imwrite(IMAGE_CONVERT_FOLDER + image_name + "_binary.png", binaryFullImage)

    # 기본 설정
    ROWS, COLS = 10, 17

    height, width = binaryFullImage.shape
    cell_h = height // ROWS
    cell_w = width // COLS

    # ====== 결과 그리드 초기화 ======
    grid = [[-1 for _ in range(COLS)] for _ in range(ROWS)]

    failCount = 0

    # ====== 셀 단위로 잘라서 OCR 수행 ======
    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * cell_w
            y1 = row * cell_h
            cell_img = binaryFullImage[y1:y1 + cell_h, x1:x1 + cell_w]

            resized = cv2.resize(cell_img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

            # resized_blurred = cv2.GaussianBlur(resized, (3, 3), 0) # 9
            # resized_blurred = cv2.bilateralFilter(resized, 9, 75, 75)
            # resized = cv2.medianBlur(resized, 7) # 3x3 메디안 필터 적용 (홀수 크기 사용

            # kernel = np.ones((2, 2), np.uint8) # 작은 커널 사용
            # esized = cv2.dilate(resized, kernel, iterations=1) # 팽창
            # resized = cv2.erode(resized, kernel, iterations=1) # 침식

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
                else:
                    print("실패")
                    failCount += 1
                    text = -1

            grid[row][col] = int(text)

            # 디버깅용 이미지 저장
            cell_filename = f"{IMAGE_DEBUG_FOLDER}cell_{row}_{col}_{text if text else 'empty'}.png"
            cv2.imwrite(cell_filename, resized)

    # ====== 결과 출력 ======
    print("Total Fail Count:", failCount)
    for row in grid:
        print(" ".join(str(cell).rjust(2) if cell != -1 else ' .' for cell in row))

    return grid
