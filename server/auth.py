# encoding: utf-8
import jwt
from models import User
import settings


def authenticate(username, password):
    user = User.select().where(User.username == username).first()

    if user and user.password.check_password(password):
        return user


def login(user):
    payload = {
        'username': user.username
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def get_user(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    user = User.select().where(User.username == payload['username']).first()
    return user


def valid_user(ws, token):
    try:
        user = get_user(token)
        if user is None:
            ws.send('O usuário desconhecido')
        return user is not None
    except jwt.DecodeError:
        ws.send('O usuário precisa estar autenticado')
    return False
