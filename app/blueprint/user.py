from flask import Blueprint, render_template, flash, redirect, url_for
from app.form.user import UserRegisterForm, UserLoginForm
from app.models.user import User
from app.extensions import db
from flask_login import login_user, logout_user, current_user
from app.utils import redirect_back

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User(user_name=form.user_name.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template("user/user_register.html", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = UserLoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            if user.check_password(password):
                login_user(user)
                flash("欢迎登录!", "info")
                return redirect_back()
            flash("密码错误!", "warning")
        else:
            flash("用户不存在!", "warning")
    return render_template("user/user_login.html", form=form)


@user_bp.route("/logout")
def logout():
    logout_user()
    flash("退出成功", "info")
    return redirect_back()