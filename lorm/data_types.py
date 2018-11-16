import datetime

import inflection


class Column:

    def __init__(self, value):
        self.type = "INT"
        self.data_type = int
        self.value = value
        self.misc = None
        self.size = 0
        self.__updatable__ = False

    @property
    def updatable(self):
        return self.value is not None and self.__updatable__

    @updatable.setter
    def updatable(self, value):
        self.__updatable__ = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.updatable = True


class Integer(Column):
    def __init__(self, value=0):
        Column.__init__(self, value)


class PrimaryKey(Column):
    def __init__(self, value=-1):
        Column.__init__(self, value)
        self.type = "INTEGER"
        self.misc = "PRIMARY KEY AUTOINCREMENT"


class String(Column):
    def __init__(self, value="", size=25):
        Column.__init__(self, value)
        self.size = size
        self.data_type = str
        self.type = "VARCHAR({})".format(size)


class Timestamp(Column):
    def __init__(self, value=datetime.datetime.now()):
        Column.__init__(self, value)
        self.data_type = float
        self.type = "TIMESTAMP"


class ForeignKey(Column):
    def __init__(self, reference, value=-1, name=None):
        Column.__init__(self, value)
        self.data_type = int
        self.type = "INTEGER"
        self.reference = reference
        if name is None:
            column = inflection.underscore(reference.__name__.lower() + "_id")
        else:
            column = name + "_id"
        self.misc = f"FOREIGN KEY({column}) REFERENCES {reference.table_name()}(id)"
