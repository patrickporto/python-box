import json
from ws4py.client.threadedclient import WebSocketClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Client(WebSocketClient, FileSystemEventHandler):
    def __init__(self, path='', *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.path = path

    def __del__(self):
        self.close(reason='Bye bye')

    def opened(self):
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()

    def on_any_event(self, event):
        src = '/'.join(event.src_path.split('/')[1:])
        self.send(json.dumps({
            'type': event.event_type,
            'path': src,
            'is_directory': event.is_directory,
        }))

    def closed(self, code, reason=None):
        self.observer.stop()
        self.observer.join()
        print "Closed down", code, reason

    def received_message(self, message):
        print(message)
