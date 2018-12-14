from lorm.active_record import ActiveRecord
from lorm.data_types import *


class User(ActiveRecord):

    def __init__(self, dictionary: dict = None):
        self.__test__ = None
        self.email = String()
        self.password = String()
        self.token = String()
        ActiveRecord.__init__(self, dictionary)
        self.__tests = self.has_many(Test)

    @property
    def tests(self):
        return self.__tests()

    @tests.setter
    def tests(self, record):
        self.__tests = record


class Test(ActiveRecord):

    def __init__(self, dictionary=None):
        self.__user__ = None
        self.id = PrimaryKey()
        self.user_id = ForeignKey(User)
        ActiveRecord.__init__(self, dictionary)
        self.__users = self.belongs_to(User)

    @property
    def user(self):
        return self.__users[0]()

    @user.setter
    def user(self, record):
        self.__users[1](record)
