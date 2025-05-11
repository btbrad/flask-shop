from flask_shop.user import user
from flask_shop import models
from flask import request

@user.route('/')
def index():
    return 'user hello!!'

@user.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')

    if not all([name, pwd]):
        return {
            'status': 0,
            'msg': '参数不足'
        }

    if len(name) > 1:
        user = models.User.query.filter_by(name=name).first()
        if user:
            if user.check_password(pwd):
                return {
                    'status': 1,
                    'msg': '登录成功',
                    'data': {
                        'name': user.name,
                        'nick_name': user.nick_name,
                        'phone': user.phone,
                        'email': user.email
                    }
                }
    return {
        'status': 0,
        'msg': '用户名或密码错误'
    }