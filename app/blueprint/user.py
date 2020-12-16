from flask import Blueprint, render_template
from app.form.user import UserRegisterForm
from app.models.user import User
from app.extensions import db

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegisterForm()
    print(form.data)
    if form.validate_on_submit():
        user = User(user_name=form.user_name.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return "注册成功!"
    return render_template("user/user_register.html", form=form)
