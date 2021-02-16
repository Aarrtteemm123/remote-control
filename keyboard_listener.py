import keyboard,threading
from global_values import Global

class KeyboardListener:
    def __run(self):
        while True:
            event = keyboard.read_event()
            Global.keyboard_events.append(event.to_json())

    def start_listen(self):
        threading.Thread(target=self.__run).start()
