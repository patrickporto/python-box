from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


def websocket_app(environ, start_response):
    ws = environ["wsgi.websocket"]
    message = ws.receive()
    print(message)
    ws.send(message)

server = pywsgi.WSGIServer(
    ('0.0.0.0', 9000),
    websocket_app,
    handler_class=WebSocketHandler,
)
server.serve_forever()
