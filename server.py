import json
import os
import shutil
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


DIRECTORY_STORAGE = '/tmp/storage'


def on_created(path, is_directory, file_content):
    if is_directory:
        os.makedirs(path)
    else:
        try:
            f = open(os.path.join(DIRECTORY_STORAGE, path), "w+")
            f.write(file_content)
            f.close()
        except IOError as e:
            print('\033[91m{0}\033[0m'.format(e))


def on_modified(path, is_directory, file_content):
    if not is_directory:
        try:
            f = open(os.path.join(DIRECTORY_STORAGE, path), "w")
            f.write(file_content)
            f.close()
        except IOError as e:
            print('\033[91m{0}\033[0m'.format(e))


def on_deleted(path, is_directory):
    path = os.path.join(DIRECTORY_STORAGE, path)
    if is_directory:
        shutil.rmtree(path, True)
    else:
        try:
            os.remove(path)
        except OSError:
            pass


def on_moved(src_path, dest_path):
    src_path = os.path.join(DIRECTORY_STORAGE, src_path)
    dest_path = os.path.join(DIRECTORY_STORAGE, dest_path)
    shutil.move(src_path, dest_path)


def websocket_app(environ, start_response):
    ws = environ["wsgi.websocket"]
    while not ws.closed:
        message = ws.receive()
        if message:
            data = json.loads(message)
            print(data)
            if data['type'] == 'created':
                on_created(data['src_path'], data['is_directory'], data['file_content'])
            if data['type'] == 'modified':
                on_modified(data['src_path'], data['is_directory'], data['file_content'])
            if data['type'] == 'deleted':
                on_deleted(data['src_path'], data['is_directory'])
            if data['type'] == 'moved':
                on_moved(data['src_path'], data['dest_path'])

server = pywsgi.WSGIServer(
    ('0.0.0.0', 9000),
    websocket_app,
    handler_class=WebSocketHandler,
)
server.serve_forever()
