from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  DataRequired, Length

from app.Model.models import Review

class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  
    submit = SubmitField('Post')
    body = TextAreaField('Body', [Length(min=1, max=1500)])