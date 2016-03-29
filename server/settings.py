import os

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = 'dnqe3c862oj5VO0TpihBVgB4x6u8PiVo'

DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'banco de dados.db')
    }
}
