from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)

class Config:
    # 配置mysql参数
    MYSQL_DIALECT = 'mysql'
    MYSQL_DRIVER = 'pymysql'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'rootpassword'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'shop_env'
    MYSQL_CHARSET = 'utf8mb4'


    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = os.urandom(16)

    DEBUG = True

app.config.from_object(Config)

db = SQLAlchemy(app)


manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

@app.route('/')
def index():
  return 'Hello World!'

if __name__ == '__main__':
  app.run()