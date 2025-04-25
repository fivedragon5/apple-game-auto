from config import IMAGE_SCREENSHOT_FOLDER, SCREENSHOT_OFFSET_X, SCREENSHOT_OFFSET_Y, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT
import pyautogui
import cv2

# 스크린샷 찍기
def take_screenshot(fileName):
    screenshot = pyautogui.screenshot(region=(SCREENSHOT_OFFSET_X, SCREENSHOT_OFFSET_Y, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))
    screenshot.save(IMAGE_SCREENSHOT_FOLDER + fileName + ".png")
    print("스크린샷 저장 완료! 파일 이름:", fileName, "확장자: png")

# 스크린샷 로드
def load_screenshot(fileName):
    image = cv2.imread(IMAGE_SCREENSHOT_FOLDER + fileName)
    return image
