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
    """
    The `PasswordValid` class represents a custom validator for password
    fields in a FlaskForm.

    Attributes: - message (str): The error message to display if the
    password is invalid.

    Methods: - __init__(self, message: str = None): Initializes the
    PasswordValid instance with an optional error message. - __call__(self,
    form, field): A callable method that performs the validation on the field.

    Example Usage: password_field = PasswordField('Password', validators=[
    PasswordValid()])

    The `PasswordValid` class is used as a validator for password fields in
    a FlaskForm. It uses the `PasswordValidator` library to validate the
    password based on the specified criteria. The password must contain at
    least 8 characters, with at least one uppercase letter, one lowercase
    letter, and one digit.

    The `PasswordValid` class implements the `__call__` method, which
    validates the password field data. If the password is invalid, it raises
    a `ValidationError` with the specified error message.
    """

    def __init__(self, message: str = None):
        """

            Initialize a PasswordValid object.

            :param message (str): The error message to be displayed if the
            password validation fails. Defaults to None.

        """
        if not message:
            message = (u'Your password must contain an uppercase letter, '
                       u'lowercase letter, digit and be at least 8 characters '
                       u'long.')
        self.message = message

    def __call__(self, form, field):
        """

        This `PasswordValid` class is a callable class that implements
        the `__call__` method. The `__call__` method is invoked when an
        instance of `PasswordValid` is called as a function.

        Parameters:
            - form: The form object that contains the field being validated.
            - field: The field object being validated.

        Raises:
            - ValidationError: If the field data does not meet the
            password validation criteria.

        Example usage:
            # Create an instance of PasswordValid
            password_validator = PasswordValid()

            # Pass the password field and the form object to the
            password_validator
            password_validator(form, field)

            # If the password is not valid, a ValidationError will be raised

        """
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    """
    The RegistrationForm class is a FlaskForm subclass used to represent
    the registration form for users to sign up for the game application.
    It contains fields for username, password, and a submit button.

    Attributes:
        username (StringField): Field for entering a username. Required
        and must be at least 3 characters long.
        password (PasswordField): Field for entering a password.
        Required and must pass custom password validation criteria.
        submit (SubmitField): Button for submitting the registration
        form.

    Methods:
        No additional methods.
    """
    username = StringField('Username',
                           [DataRequired(message='Please provide a username.'),
                            Length(min=3,
                                   message='Your username must be a minimum '
                                           'of 3 characters.')])

    password = PasswordField('Password', [DataRequired(
        message='Please provide a password'), PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """
    The `LoginForm` class represents a login form in a Flask application.

    Attributes:
        - username (StringField): Field for entering the username.
        - password (PasswordField): Field for entering the password.
        - submit (SubmitField): Button to submit the form.

    Methods:
        __init__(self)
            - Initializes the `LoginForm`.
    """
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """

    Register Function

    This function handles the registration process for new users.

    Parameters:
    No parameters.

    Returns:
    No return value.

    Example Usage:
    register()

    """
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
    """
    The login method is responsible for handling the login functionality
    of the application. It takes no parameters and returns None.

    Usage:
        login()

    The method performs the following steps:
    1. Create an instance of the LoginForm class.
    2. Initialize the variables for username_not_found and
    incorrect_password as None.
    3. Get the list of genres from the repository.
    4. Check if the form is submitted and validate it.
    5. If the form is valid, attempt to authenticate the user.
    6. If authentication is successful, clear the session and set the
    username in the session.
    7. Redirect the user to the home page.
    8. Handle the exceptions if the username is not found or the
    password is incorrect.
    9. Render the login template with the necessary data.

    Note: This method depends on the following modules and classes:
    - games.adapters.repository
    - functools.wraps
    - flask.Blueprint
    - flask.render_template
    - flask.redirect
    - flask.url_for
    - flask.session
    - flask_wtf.FlaskForm
    - password_validator.PasswordValidator
    - wtforms.StringField
    - wtforms.PasswordField
    - wtforms.SubmitField
    - wtforms.HiddenField
    - wtforms.validators.DataRequired
    - wtforms.validators.Length
    - wtforms.validators.ValidationError
    - games.get_genres_and_urls
    - games.authentication.services
    - games.authentication.services.UnknownUserException
    - games.gameLibrary.services.get_genres

    """
    form = LoginForm()
    username_not_found = None
    incorrect_password = None
    genres = get_genres(repo.repo_instance)

    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data, repo.repo_instance)
            if user is None:
                raise UnknownUserException
            user = {'username': user.username, 'password': user.password}
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
    """
    Logout user by clearing the session and redirecting them to the
    home page.

    Returns:
        redirect: Redirects user to the home page after clearing the
         session.
    """
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    """
    Decorator function to ensure that a user is logged in before
    accessing a view.

    Args:
        view (function): The view function to be decorated.

    Returns:
        function: The decorated view function.

    Raises:
        UnknownUserException: If the logged-in user is not found in the
        database.

    Example:
        @login_required
        def dashboard():
            # Function implementation

            return render_template('dashboard.html')
    """
    @wraps(view)
    def wrapped_view(**kwargs):
        """

        This method is a decorator that wraps a Flask view function.
        It is used to enforce authentication for the wrapped view
        function. If the user is not authenticated, they will be
        redirected to the login page. If the user is authenticated but
        does not exist in the database, they will be redirected to the
        registration page.

        Parameters:
        - **kwargs: The keyword arguments passed to the wrapped view
        function.

        Return Type:
        - The return type of the wrapped view function.

        Example Usage:

        @wrapped_view
        def my_view():
            # Code for the view function

        """
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        user = services.get_user(session['username'], repo.repo_instance)
        if not user:
            session.clear()
            return redirect(url_for('authentication_bp.register'))
        return view(**kwargs)

    return wrapped_view


class WishlistForm(FlaskForm):
    """
    Represents a form for adding a game to a user's wishlist.

    Attributes:
        game_id (HiddenField): The hidden input field for storing the
        game ID.
        submit (SubmitField): The submit button for adding the game to
        the wishlist.

    """
    game_id = HiddenField('Game ID')
    submit = SubmitField('Add to Wishlist')
