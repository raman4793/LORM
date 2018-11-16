import sqlite3

__database__ = None
__models__ = None
__database_name__ = "test.db"


def initialize(models, database_name="test.sqlite3"):
    global __models__
    __models__ = models
    global __database_name__
    __database_name__ = database_name


def database():
    global __database__
    if __database__ is None:
        global __database_name__
        __database__ = sqlite3.connect(__database_name__)
        __database__.row_factory = sqlite3.Row
    return __database__


def close():
    global __database__
    __database__.close()
    __database__ = None


def migrate():
    global __models__
    for model in __models__:
        model = model()
        model.migrate()
        del model


def drop():
    global __models__
    for model in __models__:
        model = model()
        model.drop()
        del model


def reset():
    drop()
    migrate()
