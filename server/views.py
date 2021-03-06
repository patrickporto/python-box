import os
import json
import shutil
from watchdog.utils.dirsnapshot import DirectorySnapshot
from auth import authenticate, login
from models import FileUploaded


def _writefile(path, content):
    try:
        f = open(path, "wb+")
        f.write(content)
        f.close()
    except IOError as e:
        print('\033[91m{0}\033[0m'.format(e))


def on_created(path, is_directory, file_content, user):
    if is_directory:
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        _writefile(path, file_content)
    (file_uploaded, created) = FileUploaded.get_or_create(
        path=path,
    )
    file_uploaded.user = user
    file_uploaded.save()


def on_modified(path, is_directory, file_content, user):
    if not is_directory:
        _writefile(path, file_content)
        file_uploaded = FileUploaded.get(
            path=path,
        )
        file_uploaded.user = user
        file_uploaded.save()


def on_deleted(path, is_directory):
    path = path
    if is_directory:
        shutil.rmtree(path, True)
    else:
        try:
            os.remove(path)
        except OSError:
            pass
    file_uploaded = FileUploaded.get(
        path=path,
    )
    file_uploaded.delete_instance()


def on_moved(src_path, dest_path):
    if os.path.exists(src_path):
        shutil.move(src_path, dest_path)
        file_uploaded = FileUploaded.get(
            path=src_path,
        )
        file_uploaded.path = dest_path
        file_uploaded.save()


def monitor_events(ws, data, directory_storage, user):
    data['src_path'] = os.path.join(directory_storage, data['src_path'])
    data['dest_path'] = os.path.join(directory_storage, data['dest_path'])
    data['file_content'] = data['file_content'].decode('uu')
    if data['type'] == 'created':
        on_created(data['src_path'], data['is_directory'], data['file_content'], user)
    elif data['type'] == 'modified':
        on_modified(data['src_path'], data['is_directory'], data['file_content'], user)
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


def pull(ws, data, directory_storage):
    for path in data:
        path_root = os.path.join(directory_storage, path)
        data = {
            'action': 'created',
            'src_path': path,
            'is_directory': os.path.isdir(path_root),
            'file_content': '',
        }
        if not data['is_directory']:
            data['file_content'] = open(path_root, 'rb').read()
        data['file_content'] = data['file_content'].encode('uu')
        ws.send(json.dumps(data))


def push(ws, data, directory_storage, user):
    data['src_path'] = os.path.join(directory_storage, data['src_path'])
    data['file_content'] = data['file_content'].decode('uu')
    on_created(data['src_path'], data['is_directory'], data['file_content'], user)


def get_snapshot(ws, directory_storage):
    snapshot = DirectorySnapshot(path=directory_storage, recursive=True)
    paths = []
    for p in snapshot.paths:
        path = p[len(directory_storage) + 1:]
        if path:
            paths.append(path)
    data = {
        'snapshot': paths,
    }
    ws.send(json.dumps(data))


def get_list(ws, directory_storage):
    data = []
    for uploaded in FileUploaded.select():
        data.append({
            'user': uploaded.user.username,
            'path': uploaded.path[len(directory_storage) + 1:],
            'date_created': str(uploaded.date_created),
            'last_update': str(uploaded.last_update),
        })
    ws.send(json.dumps(data))
