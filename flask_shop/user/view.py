import re
from flask_shop.user import user, user_api
from flask_shop import models, db
from flask import request
from flask_restful  import Resource

@user.route('/')
def index():
    return 'user hello!!'

class User(Resource):
    def get(self):
        pass

    def post(self):
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        real_pwd = request.form.get('real_pwd')
        nick_name = request.form.get('nick_name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if not all([name, pwd, real_pwd]):
            return {
                'status': 0,
                'msg': '参数不足'
            }
        if len(name) < 1:
            return {
                'status': 10011,
                'msg': '用户名长度不能小于1'
            }
        if len(pwd) < 2:
            return {
                'status': 10012,
                'msg': '密码长度不能小于2'
            }
        if pwd != real_pwd:
            return {
                'status': 10013,
                'msg': '两次密码不一致'
            }
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return {
                'status': 10014,
                'msg': '手机号格式错误'
            }
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return {
                'status': 10015,
                'msg': '邮箱格式错误'
            }
        try:
            user = models.User(name=name, password=pwd, nick_name=nick_name, email=email, phone=phone)
            db.session.add(user)
            db.session.commit()
            return {
                'status': 200,
                'msg': '注册成功'
            }
        except Exception:
            return {
                'status': 10000,
                'msg': '注册失败'
            }            
        

user_api.add_resource(User, '/user')


@user.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')

    if not all([name, pwd]):
        return {
            'status': 10000,
            'msg': '参数不足'
        }

    if len(name) > 1:
        user = models.User.query.filter_by(name=name).first()
        if user:
            if user.check_password(pwd):
                return {
                    'status': 200,
                    'msg': '登录成功',
                    'data': {
                        'name': user.name,
                        'nick_name': user.nick_name,
                        'phone': user.phone,
                        'email': user.email
                    }
                }
    return {
        'status': 10000,
        'msg': '用户名或密码错误'
    }