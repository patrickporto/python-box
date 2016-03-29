# encoding: utf-8
import json
import os
import shutil
from ws4py.client.threadedclient import WebSocketClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot
from utils import force_unicode
from message import Message
from session import session


def _writefile(path, content):
    try:
        f = open(path, "wb+")
        f.write(content)
        f.close()
    except IOError as e:
        print('\033[91m{0}\033[0m'.format(e))


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
        self.send(Message(action='check-login').dumps())
        self.send(Message(action='get-snapshot').dumps())
        self.observer.start()

    def received_message(self, message):
        self.observer.stop()
        self.observer.join()
        data = json.loads(message.data)
        error = data.get('error')
        server_snapshot = data.get('snapshot')
        action = data.get('action')
        if error:
            print(error)
            self.close()
        elif server_snapshot is not None:
            client_snapshot = []
            for p in DirectorySnapshot(self.path).paths:
                path = p[len(self.path) + 1:]
                if path:
                    client_snapshot.append(force_unicode(path))
            self.sync(server_snapshot, client_snapshot)
        elif action == 'created':
            src_path = os.path.join(self.path, data.get('src_path'))
            file_content = data.get('file_content').decode('uu')
            if data.get('is_directory') and not os.path.exists(src_path):
                os.makedirs(src_path)
            elif not os.path.exists(src_path):
                _writefile(src_path, file_content)
        elif action == 'modified':
            src_path = os.path.join(self.path, data.get('src_path'))
            if not data.get('is_directory') and os.path.exists(src_path):
                file_content = data.get('file_content').decode('uu')
                _writefile(src_path, file_content)
        elif action == 'deleted':
            src_path = os.path.join(self.path, data.get('src_path'))
            if data.get('is_directory'):
                shutil.rmtree(src_path, True)
            else:
                try:
                    os.remove(src_path)
                except OSError:
                    pass
        elif action == 'moved':
            src_path = os.path.join(self.path, data['src_path'])
            dest_path = os.path.join(self.path, data['dest_path'])
            if os.path.exists(src_path):
                shutil.move(src_path, dest_path)
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()

    def sync(self, server_snapshot, client_snapshot):
        server_created = [item for item in server_snapshot if not item in client_snapshot]
        client_created = [item for item in client_snapshot if not item in server_snapshot]
        print('sincronizando')
        print('baixa {0} novos arquivos'.format(len(server_created)))
        self.send(Message(action='pull', content=server_created).dumps())
        print('subindo {0} novos arquivos'.format(len(client_created)))
        for path in client_created:
            path_root = os.path.join(self.path, path)
            data = {
                'src_path': path,
                'is_directory': os.path.isdir(path_root),
                'file_content': '',
            }
            if not data['is_directory']:
                data['file_content'] = open(path_root, 'rb').read()
            data['file_content'] = data['file_content'].encode('uu')
            self.send(Message(action='push', content=data).dumps())


def start_server(path, host, port):
    try:
        ws = Client(
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
            session['user'] = token
            print("autenticado com sucesso.")
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
