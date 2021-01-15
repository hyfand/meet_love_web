from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

class ShareForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired(), Length(max=100)])
    content = TextAreaField("正文", validators=[DataRequired()])
    submit = SubmitField("发布")
