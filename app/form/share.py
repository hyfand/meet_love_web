from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_ckeditor import CKEditorField

class ShareForm(FlaskForm):
    content = TextAreaField("正文", validators=[DataRequired(), Length(max=1000)])
    img = FileField("配图 (非必选)", validators=[FileAllowed(["jpg", "gif", "png", "jpeg"], message="必须是图片,(jpg, gif, png, jpeg)")])
    submit = SubmitField("发布")


class ShareDeleteForm(FlaskForm):
    submit = SubmitField("删除")
