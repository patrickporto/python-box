from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import Model
from settings import DATABASES

database = SqliteExtDatabase(DATABASES['default']['NAME'])


class BaseModel(Model):
    class Meta:
        database = database
