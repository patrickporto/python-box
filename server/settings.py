import os

BASE_DIR = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'banco de dados.db')
    }
}
