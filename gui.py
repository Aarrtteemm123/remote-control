import json
import pickle
import time
import requests

import PySimpleGUI as sg
import ctypes
from server import *
import cv2
import keyboard as keyboard
import numpy
import pyautogui
from screen_viewer import ScreenViewer

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
            [sg.Radio('I\'m share a screen', "RADIO1",enable_events=True,key='-SHARE-', default=True),
             sg.Radio('I\'m control a screen', "RADIO1",enable_events=True,key='-CONTROL-')],
            [sg.Text('Local IP:               ',key='local ip label'), sg.Input(tooltip='IP computer in your local network',default_text='192.168.0.106',key='local ip')],
            [sg.Text('Remote IP:            ',key='remote ip label'), sg.Input(tooltip='Global IP remote computer',default_text='192.168.0.106',key='remote ip')],
            [sg.Text('Local port:             '), sg.Input(tooltip='Port of your server',default_text='65432',key='local port')],
            [sg.Text('Remote port:          '), sg.Input(tooltip='Port of remote server',default_text='65432',key='remote port')],
            [sg.Button('Start', key='-START-', disabled=True, size=(100, 2))],
            [sg.Button('Run server', key='-RUN-SERVER-', size=(100, 2))],
            [sg.Button('Test connection',key='-TEST-CONNECT-',disabled=True, size=(100, 2))],
            [sg.Button('Exit',key='-EXIT-', size=(100, 2))]
        ]
        self.__window = sg.Window('Computer remote control', self.__layout, size=(500, 600), icon='icon.ico')

    def start(self):
        sg.theme()   # Add a touch of color
        while True:
            event, values = self.__window.read(timeout=10)
            #print(values)
            if event == sg.WIN_CLOSED or event == '-EXIT-': # if user closes window or clicks cancel
                if Global.is_server_running:
                    requests.get(f'http://{Global.local_ip}:{Global.local_port}/shutdown')
                break

            elif event == '-SHARE-':
                Global.role = 'share'

            elif event == '-CONTROL-':
                Global.role = 'control'

            elif event == '-START-':
                res = requests.get(f'http://{Global.remote_ip}:{Global.remote_port}/validate',data={'role':'control'})
                if res.status_code == 200:
                    if Global.role == 'share':
                        pass
                    elif Global.role == 'control':
                        pass
                else:
                    ctypes.windll.user32.MessageBoxA(None, bytes(res.text,'utf-8'), b"Error!", 0x30 | 0x0)

            elif event == '-RUN-SERVER-':
                Global.local_ip = values['local ip']
                Global.remote_ip = values['remote ip']
                Global.local_port = int(values['local port'])
                Global.remote_port = int(values['remote port'])
                Global.region = (values['-X-'],values['-Y-'],values['-WIDTH-'],values['-HEIGHT-'])
                run_server(Global.local_ip,Global.local_port)
                self.__window['-TEST-CONNECT-'].update(disabled=False)
                self.__window['-RUN-SERVER-'].update(disabled=True)
                self.__window['-SHARE-'].update(disabled=True)
                self.__window['-CONTROL-'].update(disabled=True)
                self.__window['-X-'].update(disabled=True)
                self.__window['-Y-'].update(disabled=True)
                self.__window['-WIDTH-'].update(disabled=True)
                self.__window['-HEIGHT-'].update(disabled=True)
                self.__window['-START-'].update(disabled=False)

            elif event == '-TEST-CONNECT-':
                start = time.time()
                requests.get(f'http://{Global.remote_ip}:{Global.remote_port}/ping')
                ping_ms = round((time.time() - start) * 1000, 1)
                ctypes.windll.user32.MessageBoxA(None, bytes(f"Ping: {ping_ms} ms",'utf-8'), b"Info", 0x40 | 0x0)

        self.__window.close()

Gui().start()
