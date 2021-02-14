import pickle
import time

import cv2
import keyboard
import mss
import numpy
import pyautogui


while not keyboard.is_pressed('Esc'):
    st = time.time()
    img = pyautogui.screenshot()
    frame = numpy.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print(time.time() - st)
    # execute command and send data to client