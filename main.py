
import cv2
import numpy
import pyautogui

cv2.namedWindow('Window')
cursor_img = cv2.imread("cursor.png")

while cv2.getWindowProperty('Window', 1) > 0:
    mouse_pos = pyautogui.position()
    img = pyautogui.screenshot()
    img = numpy.array(img)
    img[mouse_pos.y:mouse_pos.y + cursor_img.shape[0], mouse_pos.x:mouse_pos.x + cursor_img.shape[1]] = cursor_img
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('Window', frame)
    if not cv2.waitKey(1):
        break