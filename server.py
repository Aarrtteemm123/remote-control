from flask import Flask, request, make_response
from global_values import Global
import threading

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'Test message'

@app.route('/data', methods=['GET'])
def get_data():
    # input commands
    return 'frame'

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