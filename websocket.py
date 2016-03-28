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
        context = {
            'type': event.event_type,
            'is_directory': event.is_directory,
        }
        context['src_path'] = '/'.join(event.src_path.split('/')[1:])
        if hasattr(event, 'dest_path'):
            context['dest_path'] = '/'.join(event.dest_path.split('/')[1:])
        self.send(json.dumps(context))

    def opened(self):
        self.observer.start()

    def received_message(self, message):
        print(message)
