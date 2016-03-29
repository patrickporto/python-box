import json
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import views


def websocket_app(directory_storage):
    def wrap(environ, start_response):
        ws = environ["wsgi.websocket"]
        while not ws.closed:
            message = ws.receive()
            if message:
                message = json.loads(message)
                print(message['headers']['authorization'])
                if message['action'] == 'monitor-events':
                    views.monitor_events(ws, message['content'], directory_storage)
                elif message['action'] == 'login':
                    views.auth(ws, message['content'])
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
