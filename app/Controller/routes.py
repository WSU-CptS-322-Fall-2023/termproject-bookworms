from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from config import Config

from app import db
from app.Model.models import Review, Book, Genre, Roster
from app.Controller.forms import ReviewForm, BookForm, get_book, EmptyForm, EditForm

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
    if current_user.is_anonymous:
        return redirect(url_for('routes.index'))

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
    if current_user.is_anonymous or current_user.user_type != "Admin":
        return redirect(url_for('routes.index'))
    bform = BookForm()
    if bform.validate_on_submit():
        newBook = Book(title=bform.title.data, author=bform.author.data, year=bform.year.data.year)
        for t in bform.genre.data:
            newBook.addGenre(t)
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

@bp_routes.route('/roster/<genre_id>', methods=['GET'])
# @login_required
def roster(genre_id):
    theGenre = Genre.query.filter_by(id = genre_id).first()
    if theGenre:
        theBooks = Book.query.join(Roster).filter_by(genreid = genre_id).all()

        return render_template('roster.html', title= 'Roster', books = theBooks, genre = theGenre)
    else:
        flash('Genre with id:"' + genre_id + '"not found!')
        return redirect(url_for('routes.index'))
    

@bp_routes.route('/display_profile', methods=['GET'])
# @login_required
def display_profile():
    emptyform = EmptyForm()
    return render_template('display_profile.html', title='Display Profile', user = current_user, eform = emptyform)

@bp_routes.route('/edit_profile', methods=['GET', 'POST'])
#@login_required
def edit_profile():
    eform = EditForm()
    if request.method == 'POST' :
        # handle form submission
        if eform.validate_on_submit():
            current_user.email = eform.email.data
            current_user.set_password(eform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash("Your changes have been saved")
            return redirect(url_for('routes.display_profile'))
    elif request.method == 'GET':
        # populate user data
        eform.email.data = current_user.email
    else:
        pass
    return render_template('edit_profile.html', title='Edit Profile', form = eform)