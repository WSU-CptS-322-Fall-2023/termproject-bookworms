from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Review
from app.Controller.forms import ReviewForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    reviews = Review.query.order_by(Review.timestamp.desc())
    print(reviews)
    return render_template('index.html', title="Book App", reviews=reviews)

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