from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  DataRequired, Length

from app.Model.models import Review, Book

def get_book():
    return Book.query.all()

def get_booklabel(theBook):
    return theBook.title

class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  
    submit = SubmitField('Post')
    body = TextAreaField('Body', [Length(min=1, max=1500)]) 
    book = QuerySelectField('Book', query_factory = get_book, get_label = get_booklabel, allow_blank = False)