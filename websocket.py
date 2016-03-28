import json
from ws4py.client.threadedclient import WebSocketClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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
        print(event)
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
        self.send(json.dumps(context))

    def opened(self):
        self.observer.start()

    def received_message(self, message):
        print(message)
