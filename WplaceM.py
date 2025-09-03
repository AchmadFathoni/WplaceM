import pyautogui
import cv2
import numpy as np
import time
import subprocess
from PIL import ImageGrab

template = cv2.imread('my.png', 0)
w, h = template.shape[::-1]

def focus_window(title_pattern="Brave"):
    try:
        subprocess.run(["wmctrl", "-a", title_pattern], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def take_screenshot(path="debug_screenshot.png"):
    im = ImageGrab.grab()  # capture full screen
    im.save(path)          # save for debugging
    screenshot = np.array(im)  # convert to numpy array
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def find_and_click_captcha():
    screenshot = take_screenshot("debug_screenshot.png")
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    if loc[0].size > 0:
        x, y = loc[1][0] + w // 2, loc[0][0] + h // 2
        pyautogui.click(x, y)
        print(f"Clicked CAPTCHA at ({x}, {y})")
        return True

    print("No CAPTCHA found")
    return False

print("Starting CAPTCHA monitor. Press Ctrl+C to stop.")

while True:
    if focus_window("Brave"):
        time.sleep(1)
        if find_and_click_captcha():
            print("CAPTCHA clicked in Brave window")
        else:
            print("No CAPTCHA found in Brave window")
    else:
        print("Brave window not found")

    print("Waiting 60 seconds before next check...\n")
    time.sleep(60)
