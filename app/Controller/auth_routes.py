from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from config import Config

from app import db
from app.Model.models import User, Admin, Regular_User
from app.Controller.auth_forms import RegistrationForm, LoginForm

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

#@bp_auth.route('/register', methods=['GET', 'POST'])
#def register():
#    if current_user.is_authenticated:
#        return redirect(url_for('routes.index'))
#    rform = RegistrationForm()
#    if rform.validate_on_submit():
#        user = User(username = rform.username.data, email = rform.email.data)
#        user.set_password(rform.password.data)
#        db.session.add(user)
#        db.session.commit()
#        return redirect(url_for('routes.index'))
#    return render_template('register.html', form = rform)

@bp_auth.route('/admin_registration', methods=['GET','POST'])
def admin_registration():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    rform = RegistrationForm()
    if rform.validate_on_submit():
        new_admin = Admin(username = rform.username.data,
                          email = rform.email.data,
                          user_type = "Admin")
        new_admin.set_password(rform.password.data)
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('register.html', form = rform)

@bp_auth.route('/regular_registration', methods=['GET','POST'])
def regular_registration():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    rform = RegistrationForm()
    if rform.validate_on_submit():
        new_user = Regular_User(username = rform.username.data,
                          email = rform.email.data,
                          user_type = "Reg_User")
        new_user.set_password(rform.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('register.html', form = rform)

@bp_auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(username = lform.username.data).first()
        if(user is None) or (user.check_password(lform.password.data) == False):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember = lform.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', title = 'Sign In', form = lform)

@bp_auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))