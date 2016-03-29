# encoding: utf-8
import json
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from websocket_monitor import MonitorEvents
from auth import valid_user, get_user
import views


def websocket_app(directory_storage):
    def wrap(environ, start_response):
        ws = environ["wsgi.websocket"]
        MonitorEvents(ws, directory_storage)
        while not ws.closed:
            message = ws.receive()
            if message:
                message = json.loads(message)
                if message['action'] == 'check-login':
                    valid_user(ws, message['headers']['authorization'])
                elif message['action'] == 'monitor-events' and valid_user(ws, message['headers']['authorization']):
                    user = get_user(message['headers']['authorization'])
                    views.monitor_events(ws, message['content'], directory_storage, user)
                elif message['action'] == 'login':
                    views.auth(ws, message['content'])
                elif message['action'] == 'get-snapshot' and valid_user(ws, message['headers']['authorization']):
                    views.get_snapshot(ws, directory_storage)
                elif message['action'] == 'pull' and valid_user(ws, message['headers']['authorization']):
                    views.pull(ws, message['content'], directory_storage)
                elif message['action'] == 'push' and valid_user(ws, message['headers']['authorization']):
                    user = get_user(message['headers']['authorization'])
                    views.push(ws, message['content'], directory_storage, user)
                elif message['action'] == 'get-list' and valid_user(ws, message['headers']['authorization']):
                    views.get_list(ws, directory_storage)

    return wrap


def start_server(directory, host, port):
    server = pywsgi.WSGIServer(
        (host, port),
        websocket_app(directory),
        handler_class=WebSocketHandler,
    )
    print('Servidor executando em http://{host}:{port}/'.format(
        host=host,
        port=port,
    ))
    print('Saia do servidor com CONTROL-C.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
