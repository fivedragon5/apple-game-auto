import pyautogui
import cv2

# 스크린샷 찍기
def take_screenshot(fileName, offset_x, offset_y, width, height):
    screenshot = pyautogui.screenshot(region=(offset_x, offset_y, width, height))
    screenshot.save("../image/" + fileName + ".png")
    print("스크린샷 저장 완료! 파일 이름:", fileName, "확장자: png")

def load_screenshot(fileName):
    image = cv2.imread("../image/" + fileName)
    return image
