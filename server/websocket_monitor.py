# encoding: utf-8
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MonitorEvents(FileSystemEventHandler):
    def __init__(self, ws, path='', *args, **kwargs):
        super(MonitorEvents, self).__init__(*args, **kwargs)
        self.path = path
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()
        self.ws = ws

    def __del__(self):
        self.observer.stop()
        self.observer.join()

    def on_any_event(self, event):
        filename = event.src_path.split('/')[-1]
        if filename[0] == '.' and event.event_type != 'moved':
            return
        context = {
            'action': event.event_type,
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
        self.ws.send(json.dumps(context))
