from functools import wraps
from flask_login import current_user
from flask import flash
from app.utils import redirect_back


# 封禁状态不能访问
def no_banned_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.banned:
            flash("您的账户已经被封禁! 请联系管理")
            return redirect_back()
        return func(*args, **kwargs)
    return decorated_function