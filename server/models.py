from datetime import datetime
from peewee import CharField, DateTimeField, ForeignKeyField
from playhouse.fields import PasswordField
from db import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    password = PasswordField()


class FileUploaded(BaseModel):
    date_created = DateTimeField(default=datetime.now())
    last_update = DateTimeField()
    user = ForeignKeyField(User, related_name='user', default=None)
    path = CharField(unique=True)

    def save(self, *args, **kwargs):
        self.last_update = datetime.now()
        try:
            self.user
        except:
            self.user = User.get(username='system')
        return super(FileUploaded, self).save(*args, **kwargs)


__all__ = [User, FileUploaded]
