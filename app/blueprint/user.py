from flask import Blueprint

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route('/register')
def register():
    print(1)
    return "注册成功！"
