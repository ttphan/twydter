from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    post = TextAreaField('Create a post', validators=[
        DataRequired(),
        Length(min=1, max=140)
    ])
    submit = SubmitField('Submit post')