import json
import os
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


DIRECTORY_STORAGE = '/tmp/'


def on_deleted(path, is_directory):
    path = os.path.join(DIRECTORY_STORAGE, path)
    if is_directory:
        os.rmdir(path)
    else:
        os.remove(path)


def websocket_app(environ, start_response):
    ws = environ["wsgi.websocket"]
    data = json.loads(ws.receive())
    if data['type'] == 'DELETE':
        on_deleted(data['path'], data['is_directory'])
    ws.send(data)

server = pywsgi.WSGIServer(
    ('0.0.0.0', 9000),
    websocket_app,
    handler_class=WebSocketHandler,
)
server.serve_forever()
