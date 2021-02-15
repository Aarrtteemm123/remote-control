import json
import pickle
import time
import requests

import PySimpleGUI as sg
import ctypes

import win32api
import win32con

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
            #print(values)
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

                    while not keyboard.is_pressed('Esc'):
                        mouse_pos = pyautogui.position()
                        img = pyautogui.screenshot(region=Global.region)
                        frame = numpy.array(img)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        Global.frame = frame
                        print(Global.commands)
                        if Global.commands:
                            commands = Global.commands['mouse']
                            #pyautogui.moveTo(commands['x'],commands['y'])
                        # execute commands

                elif Global.role == 'control':
                    cv2.namedWindow('Window')
                    screensize = pyautogui.size()
                    x, y, w, h = cv2.getWindowImageRect('Window')
                    cv2.moveWindow('Window', screensize.width // 2 - w // 2, screensize.height // 2 - h // 2)

                    while cv2.getWindowProperty('Window', 1) > 0:
                        mouse_pos = pyautogui.position()
                        commands = dict(mouse={'x':mouse_pos.x,'y':mouse_pos.y})
                        res = requests.get(f'http://{Global.ip}:{Global.port}/data',data={'commands':json.dumps(commands,default=lambda x: x.__dict__())})
                        frame = pickle.loads(res.content)
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

Gui().start()
