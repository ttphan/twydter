from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from twydter_app.auth.forms import LoginForm, RegistrationForm
from twydter_app.models import User
from twydter_app.extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    # If the user is already logged in, redirect to index
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
        else:
            login_user(user, remember=form.remember_me.data)

            # Flask-Login adds next argument, enabling the user to go the page he tried to go right after
            next_page = request.args.get('next')

            # netloc is used for protection to ensure the next is in our relative space and not a malicious external site
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')

            return redirect(next_page)
    return render_template('auth/login.html', title='Sign up', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # If the user is already logged in, redirect to index
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, welcome to Twydter')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

