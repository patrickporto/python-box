# encoding: utf-8
import json
from ws4py.client.threadedclient import WebSocketClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from message import Message


class Client(WebSocketClient, FileSystemEventHandler):
    def __init__(self, path='', *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.path = path
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)

    def __del__(self):
        self.observer.stop()
        self.observer.join()
        self.close(reason='Bye bye')

    def on_any_event(self, event):
        filename = event.src_path.split('/')[-1]
        if filename[0] == '.' and event.event_type != 'moved':
            return
        context = {
            'type': event.event_type,
            'is_directory': event.is_directory,
            'file_content': '',
            'dest_path': '',
        }
        if not event.is_directory and (event.event_type == 'created' or event.event_type == 'modified'):
            context['file_content'] = open(event.src_path, 'rb').read()
        context['src_path'] = event.src_path[len(self.path) + 1:]
        is_backup = event.src_path.split('/')[-1].startswith('.goutputstream')
        if not event.is_directory and event.event_type == 'moved' and is_backup:
            context['type'] = 'modified'
            context['file_content'] = open(event.dest_path, 'rb').read()
            context['src_path'] = event.dest_path[len(self.path) + 1:]
        elif hasattr(event, 'dest_path'):
            context['dest_path'] = event.dest_path[len(self.path) + 1:]
        print('sincronizando')
        context['file_content'] = context['file_content'].encode('uu')
        self.send(Message(content=context, action='monitor-events').dumps())

    def opened(self):
        self.observer.start()

    def received_message(self, message):
        print(message)


def start_server(path, host, port):
    try:
        ws = WebSocketClient(
            url='ws://{host}:{port}/'.format(host=host, port=port),
            path=path,
            protocols=['http-only', 'chat'],
        )
        ws.connect()
        print('Sincronizando com servidor em http://{host}:{port}/'.format(
            host=host,
            port=port,
        ))
        print('Finalize a sincronização com CONTROL-C.')
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()


class AuthClient(WebSocketClient):
    def __init__(self, username, password, *args, **kwargs):
        super(AuthClient, self).__init__(*args, **kwargs)
        self.username = username
        self.password = password

    def opened(self):
        context = {
            'username': self.username,
            'password': self.password,
        }
        self.send(Message(content=context, action='login').dumps())

    def received_message(self, message):
        data = json.loads(message.data)
        token = data['token']
        if token is not None:
            print(token)
        else:
            print("O usuário e a senha estão incorretos.")
        self.close()


def login(username, password, host, port):
    try:
        ws = AuthClient(
            url='ws://{host}:{port}/'.format(host=host, port=port),
            protocols=['http-only', 'chat'],
            username=username,
            password=password,
        )
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
