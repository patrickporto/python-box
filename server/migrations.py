from models import User


def createuser_system():
    User.create(username='system', password='system')
