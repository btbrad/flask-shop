from flask_shop import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class BaseModel:
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class User(db.Model, BaseModel):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32),unique=True,nullable=False)
    pwd = db.Column(db.String(128), nullable=False)
    nick_name = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(32))

    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self, password):
        self.pwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd, password)    
    

class Menu(db.Model):
    __tablename__ = 't_menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32),unique=True,nullable=False)
    level = db.Column(db.Integer)
    path = db.Column(db.String(32))
    pid = db.Column(db.Integer)
    children = db.relationship('Menu')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'pid': self.pid,
            'children': self.get_child_list()
        }
    
    def get_child_list(self):
        obj_child = self.children
        data = []
        for o in obj_child:
            data.append(o.to_dict())
        return data    
