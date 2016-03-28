import json
import os
import shutil
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


DIRECTORY_STORAGE = '/tmp/storage'


def on_deleted(path, is_directory):
    path = os.path.join(DIRECTORY_STORAGE, path)
    if is_directory:
        shutil.rmtree(path, True)
    else:
        try:
            os.remove(path)
        except OSError:
            pass


def websocket_app(environ, start_response):
    ws = environ["wsgi.websocket"]
    while not ws.closed:
        message = ws.receive()
        if message:
            data = json.loads(message)
            if data['type'] == 'deleted':
                on_deleted(data['path'], data['is_directory'])

server = pywsgi.WSGIServer(
    ('0.0.0.0', 9000),
    websocket_app,
    handler_class=WebSocketHandler,
)
server.serve_forever()
