import json,threading
from flask import Flask, request
from keyboard import KeyboardEvent
from global_values import Global

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'Test message'

@app.route('/data', methods=['GET'])
def get_data():
    data_keyboard_events = request.form.get('keyboard_events')
    data_mouse_events = request.form.get('mouse_events')
    if data_keyboard_events:
        keyboard_events_json_lst = json.loads(data_keyboard_events)
        Global.keyboard_events = [KeyboardEvent(**json.loads(event)) for event in keyboard_events_json_lst]
    if data_mouse_events:
        mouse_events_json_lst = json.loads(data_mouse_events)
        Global.mouse_events = [json.loads(event) for event in mouse_events_json_lst]
    return open('screenshot.jpg','rb').read()

@app.route('/')
def hello():
    return 'Hello!'

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server = request.environ.get('werkzeug.server.shutdown')
    if shutdown_server is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_server()
    return 'Server shutting down...'

def run_server(host, port):
    if not Global.is_server_running:
        Global.is_server_running = True
        threading.Thread(target=app.run,args=(host, port)).start()
    else:
        raise Exception('Server is already running')