import json
from pynput.mouse import Listener
from global_values import Global

class MouseListener:

    def __on_move(self, x, y):
        Global.mouse_events.append(json.dumps({'event_name':'move', 'x':x, 'y':y}))

    def __on_click(self, x, y, button, pressed):
        but = ''
        if button.left == button:
            but = 'left'
        if button.right == button:
            but = 'right'
        Global.mouse_events.append(json.dumps({'event_name':'click', 'x':x, 'y':y, 'button':but, 'pressed':pressed}))

    def __on_scroll(self, x, y, dx, dy):
        Global.mouse_events.append(json.dumps({'event_name':'scroll', 'x':x, 'y':y, 'dx':dx, 'dy':dy}))

    def start_listen(self):
        listener = Listener(
            on_move=self.__on_move,
            on_click=self.__on_click,
            on_scroll=self.__on_scroll)
        listener.start()