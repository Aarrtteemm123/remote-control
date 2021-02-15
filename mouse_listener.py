import threading
import time

from pynput.mouse import Listener

class MouseEvent:
    def __init__(self,name):
        pass

class MouseListener:

    def __on_move(self, x, y):
        print("Mouse moved to ({0}, {1})".format(x, y))

    def __on_click(self, x, y, button, pressed):
        print('Mouse clicked at ({0}, {1}) with {2},{3}'.format(x, y, button, pressed))

    def __on_scroll(self, x, y, dx, dy):
        print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

    def start_listen(self):
        listener = Listener(
            on_move=self.__on_move,
            on_click=self.__on_click,
            on_scroll=self.__on_scroll)
        listener.start()

ml = MouseListener()
ml.start_listen()
time.sleep(10)