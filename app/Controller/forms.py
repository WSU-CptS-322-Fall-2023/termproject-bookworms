from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, FileField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Review, Book, Year, Genre, User

def get_book():
    # return Book.query.all()
    return Book.query.filter(Book.posted == True).all()
    # return session.query(Book).filter(Book.suggested_by.is_(None)).all()

def get_suggestions():
    return Book.query.filter(Book.posted == False).all()

def get_booklabel(theBook):
    return theBook.title

def get_year():
    return Year.query.all()

def get_year_label(theYear):
    return theYear.year

def get_genre():
    return Genre.query.all()

def get_genrelabel(theGenre):
    return theGenre.name

class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  
    submit = SubmitField('Post')
    body = TextAreaField('Body', [Length(min=1, max=1500)]) 
    # book = QuerySelectField('Book', query_factory = get_book, get_label = get_booklabel, allow_blank = False)
    # body = TextAreaField('Body', [Length(min=1, max=1500)])

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    cover = FileField('Browse Image')
    author = StringField('Author', validators=[DataRequired()])
    year = QuerySelectField('Year', query_factory = get_year, get_label = get_year_label, allow_blank = False)
    genre = QuerySelectMultipleField('Genres', query_factory =get_genre, get_label=get_genrelabel, 
                                   widget=ListWidget(prefix_label=False), option_widget = CheckboxInput())

    #body = TextAreaField('Body', [Length(min=1, max=100000)])    not sure how we'll uupload the body
    submit = SubmitField('Add')

class EditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        users = User.query.filter_by(email = email.data).all()
        for user in users:
            if (user.id != current_user.id):
                raise ValidationError('The email is already in use with another acount! Please use a different email address.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class EditSuggestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    cover = FileField('Browse Image')
    author = StringField('Author', validators=[DataRequired()])
    year = QuerySelectField('Year', query_factory = get_year, get_label = get_year_label, allow_blank = False)
    genre = QuerySelectMultipleField('Genres', query_factory =get_genre, get_label=get_genrelabel, 
                                   widget=ListWidget(prefix_label=False), option_widget = CheckboxInput())
    submit = SubmitField('Submit')
