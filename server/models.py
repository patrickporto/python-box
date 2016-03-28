from peewee import CharField
from playhouse.fields import PasswordField
from db import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    password = PasswordField()


__all__ = [User]
