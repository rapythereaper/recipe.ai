from peewee import *
from peewee import Expression # the building block for expressions
import bcrypt
import os
import datetime as dt
import secrets

user_db = SqliteDatabase('User.db')
master_db=SqliteDatabase('Master.db')



class User(Model):
    phone_num = CharField()
    u_name= CharField()
    password=CharField()

    def set_password(self,s):
        if(s!=None ):
            self.password=bcrypt.hashpw(s.encode(),bcrypt.gensalt(5))
            return True
        return False

    def check_password(self,s):
        if(s!=None):
            if bcrypt.checkpw(s.encode(),self.password.encode()):
                return True
        return False
    def to_dict(self):
        return {"id":self.id,"u_name":self.u_name,"phone_num":self.phone_num}
    


    class Meta:
        database = user_db # This model uses the "people.db" database.

class MealPlan(Model):
    day = CharField()
    time= CharField()
    food=CharField()
    u_id=CharField()


    def to_dict(self):
        return {"id":self.id,"day":self.day,"food":self.food,"time":self.time}

    class Meta:
        database = master_db # This model uses the "people.db" database.


class Inventory(Model):
    status= CharField()
    label = CharField()
    api_key=CharField()
    u_id=CharField()

    def to_dict(self):
        return {"id":self.id,"status":self.status,"label":self.label,"api_key":self.api_key}
    def gen_api_key():
        return secrets.token_urlsafe(16)
    class Meta:
        database = master_db # This model uses the "people.db" database.

def start():
    if(not os.path.isfile("./User.db")):
        user_db.create_tables([User])

    if(not os.path.isfile("./Master.db")):
        master_db.create_tables([MealPlan,Inventory])

start()