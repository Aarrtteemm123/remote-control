import cv2, pyautogui, ctypes, numpy, threading

class ScreenViewer:
    def __init__(self, name: str, region: tuple = None):
        self.name = name
        self.region = region
        self.__is_running = True

    def __run(self):
        cv2.namedWindow(self.name)
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        x,y,w,h = cv2.getWindowImageRect(self.name)
        cv2.moveWindow(self.name,screensize[0]//2-w//2,screensize[1]//2-h//2)

        while self.__is_running and cv2.getWindowProperty(self.name, 1) > 0:
            img = pyautogui.screenshot(region=self.region)
            frame = numpy.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow(self.name, frame)
            if not cv2.waitKey(1):
                break

        cv2.destroyAllWindows()

    def start(self):
        threading.Thread(target=self.__run).start()

    def close(self):
        self.__is_running = False