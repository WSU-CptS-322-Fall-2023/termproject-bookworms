from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user
from config import Config
from werkzeug.utils import secure_filename
from io import BytesIO


from app import db
from app.Model.models import Review, Book, Genre, Roster, Year
from app.Controller.forms import ReviewForm, BookForm, get_book, EmptyForm, EditForm, get_suggestions

import os

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title="Book App", books = get_book())

@bp_routes.route('/postreview<book_id>', methods=['GET', 'POST'] )
def postReview(book_id):
    if current_user.is_anonymous:
        return redirect(url_for('routes.index'))

    book = Book.query.filter_by(id = book_id).first()

    rform = ReviewForm()
    if rform.validate_on_submit():
        review = Review(title = rform.title.data, body = rform.body.data)
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
        image = bform.cover.data
        imgPath = None
        if image:
            my_folder = 'app\\View\\static\\covers'

            if not os.path.exists(my_folder):
                os.makedirs(my_folder)
            imgPath = os.path.join(my_folder, secure_filename(image.filename))
            image.save(imgPath)
            imgPath = os.path.join('covers', secure_filename(image.filename))

        
        newBook = Book(title=bform.title.data, author=bform.author.data, year=bform.year.data.year, 
                       cover=imgPath, posted_by = current_user.username)
        for t in bform.genre.data:
            newBook.addGenre(t)

        db.session.add(newBook)
        db.session.commit()

        flash('Book "' + newBook.title + '" has been added!')

        return redirect(url_for('routes.index'))
    
    return render_template('add_book.html', form = bform)


@bp_routes.route('/suggestbook', methods=['GET', 'POST'])
#@login_required
def suggestbook():
    # if current_user.is_anonymous or current_user.user_type != "Regular_User":
    #     return redirect(url_for('routes.index'))
    bform = BookForm()
    if bform.validate_on_submit():
        image = bform.cover.data
        print(bform.cover.data)
        imgPath = None
        if image:
            my_folder = 'app\\View\\static\\covers'

            if not os.path.exists(my_folder):
                os.makedirs(my_folder)
            imgPath = os.path.join(my_folder, secure_filename(image.filename))
            image.save(imgPath)
            imgPath = os.path.join('covers', secure_filename(image.filename))

        
        newSuggestion = Book(title=bform.title.data, author=bform.author.data, year=bform.year.data.year,
                                     cover=imgPath, suggested_by=current_user.username, posted=False)
        for t in bform.genre.data:
            newSuggestion.addGenre(t)
        print(bform.genre.data)

        title = newSuggestion.title
        db.session.add(newSuggestion)
        db.session.commit()

        flash('A suggestion to add "' + title + '" has been added!')

        return redirect(url_for('routes.index'))
    
    return render_template('add_book.html', form = bform)

@bp_routes.route('/adminSuggestions>', methods=['GET'])
def adminSuggestions():
    return render_template('adminSuggestions.html', title="Suggestions:", suggestions = get_suggestions())

@bp_routes.route('/viewSuggestion/<suggestion_id>', methods=['GET'])
def viewSuggestion(suggestion_id):
    newSuggestion = Book.query.filter_by(id = suggestion_id).first()
    return render_template('_suggestion.html', book = newSuggestion)

@bp_routes.route('/acceptSuggestion/<suggestion_id>', methods=['GET', 'POST'])
def acceptSuggestion(suggestion_id):
    newSuggestion = Book.query.filter_by(id = suggestion_id).first()
    newBook = Book(title=newSuggestion.title, author=newSuggestion.author, year=newSuggestion.year, cover=newSuggestion.cover,
                    genres = newSuggestion.genres, suggested_by=newSuggestion.suggested_by, posted_by = current_user.username)

    db.session.add(newBook)
    db.session.commit()

    return redirect(url_for('routes.deleteSuggestion', suggestion_id = suggestion_id))

@bp_routes.route('/deleteSuggestion/<suggestion_id>', methods=['GET', 'POST'])
def deleteSuggestion(suggestion_id):
    newSuggestion = Book.query.filter_by(id = suggestion_id).first()
    if newSuggestion is None:
        flash('Suggestion with id "{}" not found.'.format(suggestion_id))
        return redirect(url_for('routes.adminSuggestions'))
    for g in newSuggestion.genres:
        newSuggestion.genres.remove(g)

    title = newSuggestion.title
    db.session.delete(newSuggestion)
    db.session.commit()

    flash('Suggestion "{}" was removed.'.format(title))
    return redirect(url_for('routes.adminSuggestions'))

@bp_routes.route('/reviews<book_id>', methods=['GET'])
#@login_required
def reviews(book_id):
    book = Book.query.filter_by(id = book_id).first()

    return render_template('reviews.html', reviews = book.reviews, book = book)


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

@bp_routes.route('/editSuggestion/<suggestion_id>', methods=['GET', 'POST'])
#@login_required
def editSuggestion(suggestion_id):
    suggestion = Book.query.filter_by(id = suggestion_id).first()
    sform = BookForm()
    if request.method == 'POST' :
        # handle form submission
        if sform.validate_on_submit():
            suggestion.title = sform.title.data
            image = sform.cover.data
            if image:
                my_folder = 'app\\View\\static\\covers'

                # if image.filename not in my_folder:
                if not os.path.exists(my_folder):
                    os.makedirs(my_folder)
                # if not os.path.exists(my_folder + '\\' + image.filename):

                imgPath = os.path.join(my_folder, secure_filename(image.filename))
                image.save(imgPath)
                imgPath = os.path.join('covers', secure_filename(image.filename))
                suggestion.cover = imgPath
            
            suggestion.author = sform.author.data
            suggestion.year = sform.year.data.year
            suggestion.posted = True
            suggestion.posted_by = current_user.username
            for t in sform.genre.data:
                if  not Roster.query.filter_by(bookid=suggestion.id, genreid=t.id).first():
                    suggestion.addGenre(t)
        
            db.session.add(suggestion)
            db.session.commit()

            flash("Your changes have been saved")
            return redirect(url_for('routes.adminSuggestions'))
    elif request.method == 'GET':
        sform.title.data = suggestion.title
        sform.author.data = suggestion.author
        sform.year.data = Year.query.filter_by(year = suggestion.year).first()
        sform.genre.data = [Genre.query.filter_by(id = g.genreid).first() for g in suggestion.genres]

    else:
        pass
    return render_template('editSuggestion.html', title='Edit Suggestion', form = sform)

@bp_routes.route('/deleteBook/<book_id>', methods=['DELETE','POST'])
def deleteBook(book_id):
    if current_user.user_type != "Admin":
        return redirect(url_for('routes.index'))
    book = Book.query.get(book_id)
    if book != None:
        for g in book.genres:
            book.genres.remove(g)
        db.session.commit()
        for r in book.reviews:
            book.reviews.remove(r)
        db.session.commit()
        db.session.delete(book)
        db.session.commit()
        flash(book.title + ' has been deleted')
    return redirect(url_for('routes.index'))

@bp_routes.route('/deletereview/<review_id>', methods=['DELETE', 'POST'])
def deleteReview(review_id):
    if current_user.user_type != "Admin":
        return redirect(url_for('routes.index'))
    review = Review.query.get(review_id)
    if review != None:
        db.session.delete(review)
        db.session.commit()
    return redirect(url_for('routes.index'))