import io
import time,requests,ctypes,cv2,keyboard,numpy,pyautogui
import PySimpleGUI as sg
from PIL import Image, ImageFile

from keyboard_listener import KeyboardListener
from mouse_listener import MouseListener
from server import *

def make_screenshots(filename: str,quality: int):
    while True:
        mouse_pos = pyautogui.position()
        img = pyautogui.screenshot(region=Global.region)
        img = cv2.circle(numpy.array(img), (mouse_pos.x,mouse_pos.y), 5, (255,0,0), -1)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

class Gui:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Gui, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        screensize = pyautogui.size()
        self.__layout = [
            [sg.Text('Main menu', justification='center', font='20', size=(100, 1))],
            [sg.Slider(range=(0,screensize.width),tooltip='Start x', default_value=0, key='-X-',
                       size=(100,15),pad=(10,0), orientation='horizontal', font=('Helvetica', 12))],
            [sg.Slider(range=(0,screensize.height),tooltip='Start y', default_value=0, key='-Y-',
                       size=(100,15),pad=(10,0), orientation='horizontal', font=('Helvetica', 12))],
            [sg.Slider(range=(1,screensize.width), pad=(10,5), tooltip='window record width', default_value=screensize.width, key='-WIDTH-',
                    size=(100,15), orientation='horizontal', font=('Helvetica', 12))],
            [sg.Slider(range=(1,screensize.height),tooltip='window record height', default_value=screensize.height, key='-HEIGHT-',
                       size=(100,15),pad=(10,5), orientation='horizontal', font=('Helvetica', 12))],
            [sg.Radio('I\'m share a screen (Server)', "RADIO1",enable_events=True,key='-SHARE-', default=True),
             sg.Radio('I\'m control a screen (Client)', "RADIO1",enable_events=True,key='-CONTROL-')],
            [sg.Text('IP:               ',key='local ip label'), sg.Input(default_text='192.168.0.106',key='ip')],
            [sg.Text('Port:             '), sg.Input(default_text='65432',key='port')],
            [sg.Button('Start', key='-START-', disabled=True, size=(100, 2))],
            [sg.Button('Apply', key='-APPLY-', size=(100, 2))],
            [sg.Button('Test connection',key='-TEST-CONNECT-',disabled=True, size=(100, 2))],
            [sg.Button('Exit',key='-EXIT-', size=(100, 2))]
        ]
        self.__window = sg.Window('Computer remote control', self.__layout, size=(500, 600), icon='icon.ico')

    def start(self):
        sg.theme()   # Add a touch of color
        while True:
            event, values = self.__window.read(timeout=10)
            if event == sg.WIN_CLOSED or event == '-EXIT-': # if user closes window or clicks cancel
                if Global.is_server_running:
                    requests.get(f'http://{Global.ip}:{Global.port}/shutdown')
                break

            elif event == '-SHARE-':
                Global.role = 'share'

            elif event == '-CONTROL-':
                Global.role = 'control'

            elif event == '-START-':
                self.__window.hide()
                if Global.role == 'share':
                    threading.Thread(target=make_screenshots,args=('screenshot.jpg',50)).start()

                    while not keyboard.is_pressed('Esc'):
                        keyboard.play(Global.keyboard_events)
                        Global.keyboard_events.clear()
                        #Global.mouse_events = []
                        for event in Global.mouse_events:
                            if event['event_name'] == 'click':
                                pyautogui.click(button=event['button'])
                            elif event['event_name'] == 'scroll':
                                pyautogui.scroll(event['dy'] * 5)
                            elif event['event_name'] == 'move':
                                pyautogui.moveTo(event['x'],event['y'])
                        Global.mouse_events.clear()


                elif Global.role == 'control':
                    KeyboardListener().start_listen()
                    MouseListener().start_listen()
                    cv2.namedWindow('Window')
                    screensize = pyautogui.size()
                    x, y, w, h = cv2.getWindowImageRect('Window')
                    cv2.moveWindow('Window', screensize.width // 2 - w // 2, screensize.height // 2 - h // 2)
                    ImageFile.LOAD_TRUNCATED_IMAGES = True

                    while cv2.getWindowProperty('Window', 1) > 0:
                        keyboard_events, mouse_events = Global.keyboard_events, Global.mouse_events
                        Global.keyboard_events.clear()
                        Global.mouse_events.clear()
                        res = requests.get(f'http://{Global.ip}:{Global.port}/data',data={'mouse_events':json.dumps(mouse_events),'keyboard_events':json.dumps(keyboard_events)})

                        if res.content:
                            stream = io.BytesIO(res.content)
                            frame = Image.open(stream).convert("RGBA")
                            stream.close()
                            frame = numpy.array(frame)
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            cv2.imshow('Window', frame)
                            if not cv2.waitKey(1):
                                break

                self.__window.un_hide()

            elif event == '-APPLY-':
                Global.ip = values['ip']
                Global.port = int(values['port'])
                Global.region = (values['-X-'],values['-Y-'],values['-WIDTH-'],values['-HEIGHT-'])
                try:
                    if Global.role == 'share':
                        run_server(Global.ip,Global.port)
                except Exception as e:
                    ctypes.windll.user32.MessageBoxA(None, bytes(str(e),'utf-8'), b"Error", 0x30 | 0x0)
                self.__window['-TEST-CONNECT-'].update(disabled=False)
                self.__window['-APPLY-'].update(disabled=True)
                self.__window['-SHARE-'].update(disabled=True)
                self.__window['-CONTROL-'].update(disabled=True)
                self.__window['-X-'].update(disabled=True)
                self.__window['-Y-'].update(disabled=True)
                self.__window['-WIDTH-'].update(disabled=True)
                self.__window['-HEIGHT-'].update(disabled=True)
                self.__window['-START-'].update(disabled=False)

            elif event == '-TEST-CONNECT-':
                start = time.time()
                try:
                    requests.get(f'http://{Global.ip}:{Global.port}/ping')
                except Exception as e:
                    ctypes.windll.user32.MessageBoxA(None, bytes(str(e),'utf-8'), b"Error", 0x30 | 0x0)
                ping_ms = round((time.time() - start) * 1000, 1)
                ctypes.windll.user32.MessageBoxA(None, bytes(f"Ping: {ping_ms} ms",'utf-8'), b"Info", 0x40 | 0x0)

        self.__window.close()