from flask_login import current_user
from flask import jsonify, make_response
from flask_restx import abort
from dealeumApp.models.user import User


def login_required_restx(func):
    def inner(*args,**kwargs):
        if current_user.is_authenticated:
            print("hello1")
            return func(*args,**kwargs)
        else:
            print("hello2")
            return abort(401,"Unauthorized Access")
    return inner




def roles_accepted(*args):

    def wrap(func):
        def inner(*argsa,**kwargs):
            user = User.query.filter_by(id=current_user.get_id()).first()

            for role in user.roles:
                if role.name in args:
                    return func(*argsa,**kwargs)            
            
            return abort(401,"Unauthorized Access")
        
        inner.__name__ = func.__name__
        return inner
    return wrap

