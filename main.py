import pickle
import time

import cv2
import keyboard
import mss
import numpy
import pyautogui

from screen_viewer import ScreenViewer

sv = ScreenViewer('window',(0,0,500,600))
sv.start()
    # execute command and send data to client