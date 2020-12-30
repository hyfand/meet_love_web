from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email


class UserRegisterForm(FlaskForm):
    user_name = StringField("用户名", validators=[DataRequired()])
    nick_name = StringField("昵称", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=16), EqualTo("password_repeat")])
    password_repeat = PasswordField("确认密码", validators=[DataRequired()])
    email = StringField("邮箱", validators=[Email()])
    submit = SubmitField("注册")


class UserLoginForm(FlaskForm):
    user_name = StringField("用户名", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=16)])
    remember = BooleanField("记住我")
    submit = SubmitField("登录")