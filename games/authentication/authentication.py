from flask import (Blueprint, render_template, redirect, url_for, session,
                   request)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

import games.adapters.repository as repo
from games.authentication import services

authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')


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
                                   message='Too Small Bro!')])

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
                           handler_url=url_for('authentication_bp.register'))


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_found = None
    incorrect_password = None

    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data, repo.repo_instance)
            user = {'username': user.username, 'password': user.password}
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
                           form=form)


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('app.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)

    return wrapped_view


class WishlistForm(FlaskForm):
    game_id = HiddenField('Game ID')
    submit = SubmitField('Add to Wishlist')
