from lorm.active_record import ActiveRecord
from lorm.data_types import *


class User(ActiveRecord):

    def __init__(self):
        self.id = PrimaryKey()
        self.email = String()
        self.password = String()
        self.token = String()
        ActiveRecord.__init__(self)
