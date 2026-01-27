import pyautogui
import cv2
import numpy as np


def screenshot_screen():
    # takes a screenshot of the fullscreen
    # and return it as openCV image
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return img


if __name__ == "__main__":
    img = screenshot_screen()
    cv2.imshow("Fullscreen", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
