from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp
from flask_wtf.file import FileRequired, FileAllowed
from app.models.user import User
from wtforms.validators import ValidationError
from app.extensions import db

class AdminUserLoginForm(FlaskForm):
    admin_name = StringField("管理员", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=16)])
    remember = BooleanField("记住我")
    submit = SubmitField("登录")

    def validate_admin_name(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError('您不是管理员')

        if not user.check_password(self.password.data):
            raise ValidationError('密码错误')

    def get_user(self):
        user = db.session.query(User).filter_by(user_name=self.admin_name.data).first()
        return user