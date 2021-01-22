from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

class ShareForm(FlaskForm):
    content = TextAreaField("正文", validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField("发布")
