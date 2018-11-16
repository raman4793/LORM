from .data_types import *
from .lorm import database


class ActiveRecord:

    def __init__(self, dictionary: dict = None):
        self.__new_record__ = True
        if dictionary is None:
            self.id = PrimaryKey()
            self.created_at = Timestamp()
            self.updated_at = Timestamp()
        else:
            self.__dict__ = dictionary

    def save(self):
        if self.__new_record__:
            return self.__insert__()
        else:
            return self.__update__()

    def __insert__(self):
        self.created_at.value = datetime.datetime.now()
        self.updated_at.value = self.created_at.value
        sql = f"INSERT INTO {self.table_name()}"
        columns = " ("
        values = " VALUES("
        for key, value in self.__dict__.items():
            if value is not None and "__" not in key and key != "id":
                columns += key + ", "
                values += "'" + str(value.value) + "', "
        columns = columns[:-2] + ")"
        values = values[:-2] + ");"
        sql += columns + values
        print(f"INSERTING {sql}")
        cursor = database().cursor()
        cursor.execute(sql)
        database().commit()
        self.id.value = cursor.lastrowid
        self.__new_record__ = False
        print(f"INSERTED {self.to_s()}\n")

    def __update__(self):
        self.created_at.updatable = False
        self.updated_at.value = datetime.datetime.now()
        sql = f"UPDATE {self.table_name()} SET "
        for key, value in self.__dict__.items():
            if value is not None and "__" not in key and key != "id" and value.updatable:
                sql += key + " = '" + str(value.value) + "', "
        sql = sql[:-2] + " WHERE id='" + str(self.id.value) + "';"
        print(f"UPDATING {sql}")
        count = database().execute(sql)
        database().commit()
        print(f"UPDATED {self.to_s()}\n")

    def destroy(self):
        sql = f"DELETE FROM {self.table_name()} WHERE id={self.id.value}"
        print(f"DELETING : {sql}")
        database().execute(sql)
        database().commit()
        print(f"DELETED {self.to_s()}\n")

    def belongs_to(self, relation):
        def getter():
            relation_name = relation.__name__.lower()
            if self.__dict__["__" + relation_name + "__"] is None:
                self.__dict__["__" + relation_name] = relation.find(self.__dict__[relation_name + "_id"].value)
            return self.__dict__["__" + relation_name]

        def setter(record):
            __class_name__ = inflection.underscore(record.__class__.__name__.lower())
            self.__dict__[__class_name__ + "_id"].value = record.id.value
            self.__dict__["__" + __class_name__] = record

        return getter, setter

    def has_many(self, relation):
        def getter():
            column = f"{self.__class__.__name__.lower()}_id"
            return relation.find_by(column, self.id.value)

        return getter

    def to_s(self) -> str:
        text = self.__class__.__name__ + ": {"
        for key, value in self.__dict__.items():
            if "__" not in key:
                text += key + ": " + str(value.value) + ", "
        text = text[:-2] + "}"
        return text

    def show(self):
        print(self.to_s())

    def migrate(self):
        sql = "CREATE TABLE IF NOT EXISTS {}".format(self.table_name())
        sql += "("
        fks = ""
        for column, value in self.__dict__.items():
            if "__" not in column:
                sql += column + " "
                sql += value.type
                if value.misc is not None and type(value) is not ForeignKey:
                    sql += " " + value.misc
                if type(value) is ForeignKey:
                    fks += value.misc + ", "
                sql += ", "
        sql += fks
        sql = sql[:-2] + ");"
        print("MIGRATING : " + self.table_name() + " : " + sql + "\n")
        database().execute(sql)

    @classmethod
    def drop(cls):
        sql = f"DROP TABLE {cls.table_name()}\n"
        print("DROPPING : " + cls.table_name() + " : " + sql)
        database().execute(sql)

    @classmethod
    def table_name(cls) -> str:
        return inflection.pluralize(inflection.dasherize(cls.__name__.lower()))

    @classmethod
    def find(cls, record_id):
        sql = f"SELECT * FROM {cls.table_name()} WHERE id = {record_id}"
        return cls.__limit__(sql, 1)

    @classmethod
    def all(cls):
        sql = f"SELECT * FROM {cls.table_name()}"
        return cls.__limit__(sql)

    @classmethod
    def find_by(cls, column, value, limit=None):
        comparator = '='
        if type(value) is str:
            comparator = 'LIKE'
        sql = f"SELECT * FROM {cls.table_name()} WHERE {column}{comparator}{value}"
        return cls.__limit__(sql, limit)

    @classmethod
    def where(cls, condition, limit=None):
        sql = f"SELECT * FROM {cls.table_name()} WHERE {condition}"
        return cls.__limit__(sql, limit)

    @classmethod
    def __limit__(cls, sql, limit=None):
        if limit is not None:
            sql += " LIMIT " + str(limit)
        print(f"EXECUTING SQL QUERY : {sql}")
        cursor = database().execute(sql)
        records = cls.__map_cursor_to_object__(cursor)
        if limit is not None:
            if limit == 1:
                records = records[0]
        return records

    @classmethod
    def __map_cursor_to_object__(cls, cursor, new_record=False):
        records = []
        record = cls()
        for row in cursor.fetchall():
            for key, value in record.__dict__.items():
                if key in row.keys():
                    value.value = (row[key])
                    value.updatable = False
            record.__new_record__ = new_record
            records.append(record)
            record = cls()
        return records
