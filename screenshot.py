import cv2
import numpy
import pyautogui
import win32api

class Screenshot:
    
    @staticmethod
    def get(region):
        return pyautogui.screenshot(region=region) 
    
    @staticmethod
    def process_img(img):
        mouse_x, mouse_y = win32api.GetCursorPos()
        img = cv2.circle(numpy.array(img), (mouse_x, mouse_y), 5, (255,0,0), -1)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return frame

    @staticmethod
    def save(frame, filename, quality):
        cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])


def make_screenshots(filename: str, quality: int, region: tuple):
    while True:
        img = Screenshot.get(region)
        frame = Screenshot.process_img(img)
        Screenshot.save(frame,filename,quality)