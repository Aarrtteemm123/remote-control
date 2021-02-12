import PySimpleGUI as sg
import ctypes

import pyautogui

from client import Client
from server import Server

class Gui:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Gui, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        screensize = pyautogui.size()
        self.__layout = [
            [sg.Text('Main menu', justification='center', font='20', size=(100, 1))],
            [sg.Slider(range=(1,screensize.width), pad=(10,5), tooltip='window record width', default_value=screensize.width, key='-WIDTH-',
                    size=(100,15), orientation='horizontal', font=('Helvetica', 12))],
            [sg.Slider(range=(1,screensize.height),tooltip='window record height', default_value=screensize.height, key='-HEIGHT-',
                       size=(100,15),pad=(10,0), orientation='horizontal', font=('Helvetica', 12))],
            [sg.Radio('Server', "RADIO1", pad=(10,5), key='-SERVER_RADIO-',enable_events=True, default=True),
             sg.Radio('Client', "RADIO1", pad=(20,5), key='-CLIENT_RADIO-',enable_events=True)],
            [sg.Text('IP:               ',key='ip label'), sg.Input(key='ip',disabled=True)],
            [sg.Text('Port:            '), sg.Input(key='port')],
            [sg.Button('Run server', key='-RUN-SERVER-', size=(100, 2))],
            [sg.Button('Connect to server',key='-CONNECT-',disabled=True, size=(100, 2))],
            [sg.Button('Exit',key='-EXIT-', size=(100, 2))]
        ]
        self.__window = sg.Window('Computer remote control', self.__layout, size=(500, 470), icon='icon.ico')

    def start(self):
        sg.theme()   # Add a touch of color
        while True:
            event, values = self.__window.read(timeout=100)
            print(event)
            if event == sg.WIN_CLOSED or event == '-EXIT-': # if user closes window or clicks cancel
                break

            elif event == '-SERVER_RADIO-':
                self.__window['ip'].update(disabled=True)
                self.__window['-RUN-SERVER-'].update(disabled=False)
                self.__window['-CONNECT-'].update(disabled=True)

            elif event == '-CLIENT_RADIO-':
                self.__window['ip'].update(disabled=False)
                self.__window['-RUN-SERVER-'].update(disabled=True)
                self.__window['-CONNECT-'].update(disabled=False)

            elif event == '-RUN-SERVER-':
                pass

            elif event == '-CONNECT-':
                pass

        self.__window.close()

Gui().start()
