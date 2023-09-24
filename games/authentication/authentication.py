from functools import wraps

from flask import (Blueprint, render_template, redirect, url_for, session)
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

import games.adapters.repository as repo
from games import get_genres_and_urls
from games.authentication import services
from games.authentication.services import UnknownUserException
from games.gameLibrary.services import get_genres

authentication_blueprint = Blueprint('authentication_bp', __name__,
                                     url_prefix='/authentication')


class PasswordValid:
    def __init__(self, message: str = None):
        if not message:
            message = (u'Your password must contain an uppercase letter, '
                       u'lowercase letter, digit and be at least 8 characters '
                       u'long.')
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           [DataRequired(message='Please provide a username.'),
                            Length(min=3,
                                   message='Your username must be a minimum '
                                           'of 3 characters.')])

    password = PasswordField('Password', [DataRequired(
        message='Please provide a password'), PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None
    genres = get_genres(repo.repo_instance)

    if form.validate_on_submit():
        try:
            services.add_user(form.username.data, form.password.data,
                              repo.repo_instance)
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            username_not_unique = ('That username is already in use, '
                                   'please provide another.')

    return render_template('authentication/login_register.html',
                           title='Register', form=form,
                           username_error_message=username_not_unique,
                           handler_url=url_for('authentication_bp.register'),
                           all_genres=genres,
                           genre_urls=get_genres_and_urls())


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_found = None
    incorrect_password = None
    genres = get_genres(repo.repo_instance)

    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data, repo.repo_instance)
            if not user:
                raise UnknownUserException
            user = {'username': user['username'], 'password': user['password']}
            services.authenticate_user(user['username'], form.password.data,
                                       repo.repo_instance)

            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home'))
        except services.UnknownUserException:
            username_not_found = 'The username entered does not exist.'
        except services.AuthenticationException:
            incorrect_password = 'The password provided is incorrect.'

    return render_template('authentication/login_register.html', title='Login',
                           username_error_message=username_not_found,
                           password_error_message=incorrect_password,
                           form=form,
                           all_genres=genres,
                           genre_urls=get_genres_and_urls())


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('app.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        user = services.get_user(session['username'], repo.repo_instance)
        if not user:
            session.clear()
            return redirect(url_for('authentication_bp.register'))
        return view(**kwargs)

    return wrapped_view


class WishlistForm(FlaskForm):
    game_id = HiddenField('Game ID')
    submit = SubmitField('Add to Wishlist')
