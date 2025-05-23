from flask_shop.menu import menu, menu_api
from flask_shop import models, db
from flask import request
from flask_restful  import Resource
from flask_shop.utils.message import to_dict_msg

class Menu(Resource):
    def get(self):
        type_ = request.args.get('type')
        menu_list = []
        if type_ == 'list':
            mu = models.Menu.query.filter(models.Menu.level != 0).all()
            for m in mu:
                menu_list.append(m.to_dict())
        else:
            mu = models.Menu.query.filter(models.Menu.level == 1).all()
            for m in mu:
                menu_list.append(m.to_dict())
        return to_dict_msg(200, data=menu_list)
    
menu_api.add_resource(Menu, '/menu')    
