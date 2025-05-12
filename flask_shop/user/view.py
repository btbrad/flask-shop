import re
from flask_shop.user import user, user_api
from flask_shop import models, db
from flask import request
from flask_restful  import Resource
from flask_shop.utils.message import to_dict_msg
from flask_shop.utils.tokens import generate_auth_token, login_required

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
            return to_dict_msg(status=10000)
        if len(name) < 1:
            return to_dict_msg(status=10011)
        if len(pwd) < 2:
            return to_dict_msg(status=10012)
        if pwd != real_pwd:
            return to_dict_msg(status=10013)
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return to_dict_msg(status=10014)
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return to_dict_msg(status=10015)
        try:
            user = models.User(name=name, password=pwd, nick_name=nick_name, email=email, phone=phone)
            db.session.add(user)
            db.session.commit()
            return to_dict_msg(status=200, msg='注册成功')
        except Exception:
            return to_dict_msg(status=20000, msg='注册失败') 
        

user_api.add_resource(User, '/user')


@user.route('/login', methods=['POST'])
@login_required
def login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')

    if not all([name, pwd]):
        return to_dict_msg(status=10000)

    if len(name) > 1:
        user = models.User.query.filter_by(name=name).first()
        if user:
            if user.check_password(pwd):
                token = generate_auth_token(user.id, 1000*60*60*24*7)
                return to_dict_msg(status=200, msg='登录成功', data={'token': token})
    return to_dict_msg(status=10000, msg='用户名或密码错误')