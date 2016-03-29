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
