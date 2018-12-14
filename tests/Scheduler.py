from lorm import lorm
from .user import *

models = [User, Test]

lorm.initialize(models)

user = User()
user.email = String("test@gmail.com")
user.password = String("123456")
user.token = String("")
user.save()

user.email.value = "raman@gmail.com"
user.save()

user = User.find(1)
print(f"FOUND {user.to_s()}\n")
user.token.value = '12345654321'
user.save()
test = Test()
test.user = user
test.save()

# user.destroy()

lorm.close()
