from pywinauto import Desktop
import pyautogui
import cv2
import numpy as np
import time


template = cv2.imread('4k704y.png', 0)
w, h = template.shape[::-1]

def find_and_click_captcha():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    if loc[0].size > 0:
        x, y = loc[1][0] + w // 2, loc[0][0] + h // 2
        pyautogui.click(x, y)
        print(f"Clicked CAPTCHA at ({x}, {y})")
        return True
    return False

print("Starting CAPTCHA monitor. Press Ctrl+C to stop.")

while True:

    windows = Desktop(backend="uia").windows(title_re=".*Brave.*")
    
    for win in windows:
        try:
            win.set_focus() 
            time.sleep(1)   
            if find_and_click_captcha():
                print(f"CAPTCHA clicked in window: {win.window_text()}")
            else:
                print(f"No CAPTCHA found in window: {win.window_text()}")
        except Exception as e:
            print(f"Error with window {win.window_text()}: {e}")
    
    print("Waiting 60 seconds before next check...\n")
    time.sleep(60)  
