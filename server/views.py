import os
import json
import shutil
from auth import authenticate, login


def _writefile(path, content):
    try:
        f = open(path, "wb+")
        f.write(content)
        f.close()
    except IOError as e:
        print('\033[91m{0}\033[0m'.format(e))


def on_created(path, is_directory, file_content):
    if is_directory:
        os.makedirs(path)
    else:
        _writefile(path, file_content)


def on_modified(path, is_directory, file_content):
    if not is_directory:
        _writefile(path, file_content)


def on_deleted(path, is_directory):
    path = path
    if is_directory:
        shutil.rmtree(path, True)
    else:
        try:
            os.remove(path)
        except OSError:
            pass


def on_moved(src_path, dest_path):
    shutil.move(src_path, dest_path)


def monitor_events(ws, data, directory_storage):
    data['src_path'] = os.path.join(directory_storage, data['src_path'])
    data['dest_path'] = os.path.join(directory_storage, data['dest_path'])
    data['file_content'] = data['file_content'].decode('uu')
    if data['type'] == 'created':
        on_created(data['src_path'], data['is_directory'], data['file_content'])
    elif data['type'] == 'modified':
        on_modified(data['src_path'], data['is_directory'], data['file_content'])
    elif data['type'] == 'deleted':
        on_deleted(data['src_path'], data['is_directory'])
    elif data['type'] == 'moved':
        on_moved(data['src_path'], data['dest_path'])


def auth(ws, data):
    user = authenticate(username=data['username'], password=data['password'])
    data = {
        'token': None
    }
    if user is not None:
        data['token'] = login(user)
    ws.send(json.dumps(data))
