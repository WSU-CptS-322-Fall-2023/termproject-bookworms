from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Review, Book
from app.Controller.forms import ReviewForm, BookForm, get_book

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    # reviews = Review.query.order_by(Review.timestamp.desc())
    # theBook = Book.query.order_by(Book.timestamp.desc())

    # print(reviews)
    return render_template('index.html', title="Book App", books = get_book())

@bp_routes.route('/postreview<book_id>', methods=['GET', 'POST'] )
def postReview(book_id):
    book = Book.query.filter_by(id = book_id).first()

    rform = ReviewForm()
    if rform.validate_on_submit():
        review = Review(title = rform.title.data, body = rform.body.data)
        # db.session.add(review)
        book.reviews.append(review)
        db.session.commit()
        flash('post successfully created!')
        return redirect(url_for('routes.index')) 
    
    return render_template('create.html', book = book, form = rform)



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

@bp_routes.route('/reviews<book_id>', methods=['GET'])
#@login_required
def reviews(book_id):
    book = Book.query.filter_by(id = book_id).first()

    return render_template('_review.html', reviews = book.reviews, book = book)


@bp_routes.route('/like/<review_id> <book_id>', methods=['POST'])
# @login_required
def like(review_id, book_id):
    theReview = Review.query.filter_by(id = review_id).first()
    theReview.likes = theReview.likes + 1
    db.session.add(theReview)
    db.session.commit()

    return redirect(url_for('routes.reviews', book_id=book_id))

