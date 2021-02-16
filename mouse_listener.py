import json
import threading
import time

from pynput.mouse import Listener

from global_values import Global

class MouseEvent:
    def __init__(self, event_name, x, y):
        self._name = event_name
        self.x = x
        self.y = y

    def to_json(self):
        return json.dumps({'event_name':self._name, 'x':self.x, 'y':self.y})

class MouseMove(MouseEvent):
    def __init__(self, x, y):
        super().__init__('move', x, y)


class MouseScroll(MouseEvent):
    def __init__(self, x, y, dx, dy):
        super().__init__('scroll', x, y)
        self.dx = dx
        self.dy = dy

    def to_json(self):
        return json.dumps({'event_name':self._name, 'x':self.x, 'y':self.y, 'dx':self.dx, 'dy':self.dy})

class MouseClick(MouseEvent):
    def __init__(self, x, y, button, pressed):
        super().__init__('click', x, y)
        self.button = None
        self.pressed = pressed
        if button.left == button:
            self.button = 'left'
        if button.right == button:
            self.button = 'right'

    def to_json(self):
        return json.dumps({'event_name':self._name, 'x':self.x, 'y':self.y, 'button':self.button, 'pressed':self.pressed})

class MouseListener:

    def __on_move(self, x, y):
        print("Mouse moved to ({0}, {1})".format(x, y))
        Global.mouse_events.append(MouseMove(x,y).to_json())

    def __on_click(self, x, y, button, pressed):
        print('Mouse clicked at ({0}, {1}) with {2},{3}'.format(x, y, button, pressed))
        Global.mouse_events.append(MouseClick(x,y,button,pressed).to_json())

    def __on_scroll(self, x, y, dx, dy):
        print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
        Global.mouse_events.append(MouseScroll(x,y,dx,dy).to_json())

    def start_listen(self):
        listener = Listener(
            on_move=self.__on_move,
            on_click=self.__on_click,
            on_scroll=self.__on_scroll)
        listener.start()