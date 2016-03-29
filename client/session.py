import pickle
import os
import settings


class Session(object):
    def __init__(self):
        self._data = {}
        self._load()

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        self._data[key] = value
        self._save()

    def _load(self):
        if not (os.path.exists(settings.SESSION_NAME) and os.path.isfile(settings.SESSION_NAME)):
            self._save()
        with open(settings.SESSION_NAME, 'rb+') as f:
            self._data = pickle.load(f)

    def _save(self):
        with open(settings.SESSION_NAME, 'wb+') as f:
            pickle.dump(self._data, f)


session = Session()
