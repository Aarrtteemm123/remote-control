import json
import pickle
import threading
import time

import keyboard
from keyboard import KeyboardEvent

from global_values import Global

class KeyboardListener:
    def __run(self):
        while True:
            event = keyboard.read_event()
            Global.keyboard_events.append(event.to_json())

    def start_listen(self):
        threading.Thread(target=self.__run).start()

#KeyboardListener().start_listen()
#time.sleep(5)
#keyboard.play([KeyboardEvent(**json.loads(data)) for data in Global.keyboard_events])
