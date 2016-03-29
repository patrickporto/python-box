import json
from session import session


class Message(object):
    def __init__(self, content={}, headers={}, action='default'):
        self._action = action
        self._headers = headers
        self._content = content

    def __repr__(self):
        return self.dumps()

    def dumps(self):
        self._headers['authorization'] = session['user']
        data = {
            'action': self._action,
            'headers': self._headers,
            'content': self._content,
        }
        return json.dumps(data)

    def loads(self, message):
        data = json.loads(message)
        self._action = data['action']
        self._headers = data['headers']
        self._content = data['content']
