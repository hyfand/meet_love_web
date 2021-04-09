from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp
from flask_wtf.file import FileRequired, FileAllowed

class AdminUserLoginForm(FlaskForm):
    user_name = StringField("管理员", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=16)])
    remember = BooleanField("记住我")
    submit = SubmitField("登录")