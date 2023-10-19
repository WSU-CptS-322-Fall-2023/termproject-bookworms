from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import  DataRequired, Length 

from app.Model.models import Review, Year

def get_year():
    return Year.query.all()

def get_year_label(theYear):
    return theYear.year

class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  
    submit = SubmitField('Post')
    body = TextAreaField('Body', [Length(min=1, max=1500)])

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year = QuerySelectField('Year', query_factory = get_year, get_label = get_year_label, allow_blank = False)

    #body = TextAreaField('Body', [Length(min=1, max=100000)])    not sure how we'll uupload the body
    submit = SubmitField('Add')




