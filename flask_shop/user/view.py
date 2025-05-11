from flask_shop.user import user

@user.route('/')
def index():
    return 'user hello!!'