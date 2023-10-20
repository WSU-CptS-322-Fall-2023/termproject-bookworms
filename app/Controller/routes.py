from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Review, Book
from app.Controller.forms import ReviewForm, BookForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    reviews = Review.query.order_by(Review.timestamp.desc())
    theBook = Book.query.order_by(Book.timestamp.desc())

    print(reviews)
    return render_template('index.html', title="Book App", reviews=reviews, books = theBook.all())

@bp_routes.route('/postreview', methods=['GET', 'POST'] )
def postReview():
    rform = ReviewForm()
    if rform.validate_on_submit():
        review = Review(title = rform.title.data, body = rform.body.data)
        db.session.add(review)
        db.session.commit()
        flash('post successfully created!')
        return redirect(url_for('routes.index')) 
    return render_template('create.html', form = rform)


@bp_routes.route('/addbook', methods=['GET', 'POST'])
#@login_required
def addbook():
    bform = BookForm()
    if bform.validate_on_submit():
        newBook = Book(title=bform.title.data, author=bform.author.data, year=bform.year.data.year)
        db.session.add(newBook)
        db.session.commit()

        flash('Book "' + newBook.title + '" has been added!')

        return redirect(url_for('routes.index'))
    
    return render_template('add_book.html', form = bform)
