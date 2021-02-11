import time

import numpy as np
import pyautogui as pyautogui
import cv2

cv2.namedWindow('screenshot')

while cv2.getWindowProperty('screenshot', 1) > 0:
    # make a screenshot
    st = time.time()
    img = pyautogui.screenshot()
    # convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(img)
    # convert colors from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # show the frame
    cv2.imshow("screenshot", frame)
    # if the user clicks q, it exits
    print(time.time() - st)
    if cv2.waitKey(1) == ord("q"):
        break

# make sure everything is closed when exited
cv2.destroyAllWindows()