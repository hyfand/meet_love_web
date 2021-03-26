from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp
from flask_wtf.file import FileRequired, FileAllowed


class UserRegisterForm(FlaskForm):
    user_name = StringField("用户名(登陆用)", validators=[DataRequired()])
    nick_name = StringField("昵称", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=16), Regexp("^.*(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*?\(\)]*).*$", message="密码太简单"), EqualTo("password_repeat")])
    password_repeat = PasswordField("确认密码", validators=[DataRequired()])
    sex = SelectField("性别", coerce=int, default=1)
    email = StringField("邮箱", validators=[Email()])
    phone = StringField("电话", validators=[DataRequired(), Length(min=11, max=11), Regexp('^1[35789]\d{9}$', message="手机号码不合法")])
    manifesto = TextAreaField("个人介绍(1-500字)", validators=[DataRequired(), Length(min=1, max=500, message="请输入1-500字")])  # 个人宣言
    submit = SubmitField("注册")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sex.choices = [(0, "女生"), (1, "男生")]


class UserRegisterFormFull(FlaskForm):
    user_name = StringField("用户名", validators=[DataRequired()])
    nick_name = StringField("昵称", validators=[DataRequired()])
    real_name = StringField("姓名", validators=[DataRequired()])
    id_number = StringField("身份证号", validators=[DataRequired(), Length(min=18, max=18)])
    sex = SelectField("性别", coerce=int, default=1)
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=16), Regexp("^.*(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*?\(\)]*).*$", message="密码太简单"), EqualTo("password_repeat")])
    password_repeat = PasswordField("确认密码", validators=[DataRequired()])
    email = StringField("邮箱", validators=[Email()])
    phone = StringField("电话", validators=[DataRequired(), Length(min=11, max=11), Regexp('^1[35789]\d{9}$', message="手机号码不合法")])
    manifesto = TextAreaField("个人介绍(1-500字)",
                              validators=[DataRequired(), Length(min=1, max=500, message="请输入1-500字")])  # 个人宣言
    submit = SubmitField("注册")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sex.choices = [(0, "女生"), (1, "男生")]


class UserLoginForm(FlaskForm):
    user_name = StringField("用户名", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=16)])
    remember = BooleanField("记住我")
    submit = SubmitField("登录")


class UserChangeInfoForm(FlaskForm):
    nick_name = StringField("昵称", validators=[DataRequired()])
    email = StringField("邮箱", validators=[Email()])
    phone = StringField("电话", validators=[DataRequired(), Length(min=11, max=11), Regexp('^1[35789]\d{9}$', message="手机号码不合法")])
    manifesto = TextAreaField("个人介绍(20-500字)", validators=[DataRequired(), Length(min=20, max=500, message="请输入20-500字")])  # 个人宣言
    submit = SubmitField("确定")


class UserChangePasswordForm(FlaskForm):
    old = PasswordField("密码", validators=[DataRequired(), Length(min=8, max=16)])
    new = PasswordField("新密码", validators=[DataRequired(), Length(min=8, max=16), Regexp("^.*(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*?\(\)]*).*$", message="密码太简单"), EqualTo("new_repeat", message="密码不一致")])
    new_repeat = PasswordField("再次输入新密码", validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField("确定")


class UserAvatarForm(FlaskForm):
    image = FileField("图片上传(小于3M)", validators=[FileRequired(), FileAllowed(["jpg", "png", "jpeg", "gif", "bmp"], message="头像格式要求 jpg png jpeg gif bmp")])
    submit = SubmitField("上传头像")


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField("裁剪上传头像")