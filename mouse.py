import win32api
import win32con

class Mouse:
    @staticmethod
    def left_click(clicks=1):
        for click in range(clicks):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

    @staticmethod
    def right_click(clicks=1):
        for click in range(clicks):
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

    @staticmethod
    def press_right():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)

    @staticmethod
    def release_right():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

    @staticmethod
    def press_left():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)

    @staticmethod
    def release_left():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

    @staticmethod
    def scroll(dx, dy):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, dx, dy)

    @staticmethod
    def move_to(x,y):
        win32api.SetCursorPos((x,y))