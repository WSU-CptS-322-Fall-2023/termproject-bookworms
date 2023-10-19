from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  DataRequired, Length 

from app.Model.models import Review

class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  
    submit = SubmitField('Post')
    body = TextAreaField('Body', [Length(min=1, max=1500)])

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    #year = SelectField('Year', choices=[(1,'2023'), (2, '2022'), (3, '2021')])

    #body = TextAreaField('Body', [Length(min=1, max=100000)])    not sure how we'll uupload the body
    submit = SubmitField('Add')
