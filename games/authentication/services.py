from werkzeug.security import generate_password_hash, check_password_hash

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class InvalidUsernameException(Exception):
    pass


class InvalidPassException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):
    """
    Add User Method

    Adds a new User to the repository.

    Parameters:
    - username (str): The username of the user.
    - password (str): The password of the user.
    - repo (AbstractRepository): The repository where the user will be
    added.

    Raises:
    - NameNotUniqueException: If a user with the same username already
    exists in the repository.
    - InvalidUsernameException: If the username is not a non-empty
    string.
    - InvalidPassException: If the password is not a non-empty string
    with length greater than 6.

    Returns:
    None
    """
    user = repo.get_user(username)
    print(user)
    if user is not None:
        raise NameNotUniqueException
    if isinstance(username, str) and username.strip():
        pass
    else:
        raise InvalidUsernameException
    if isinstance(password, str) and len(password.strip()) > 6:
        pass
    else:
        raise InvalidPassException

    password_hash = generate_password_hash(password)
    repo.add_user(User(username, password_hash))


def get_user(username: str, repo: AbstractRepository):
    """
    Retrieve a user from the repository based on the given username.

    Parameters:
    - username (str): The username of the user to retrieve.
    - repo (AbstractRepository): The repository to retrieve the user
    from.

    Returns:
    - User: The user object retrieved from the repository.

    Note:
    - Raises an exception if the user with the given username is not
    found in the repository.
    """
    user = repo.get_user(username.lower())
    # if user is None:
    #     raise UnknownUserException

    # return user_to_dict(user)
    return user


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    """

    Authenticate a user with a given username and password.

    Parameters:
    ----------
    username: str
        The username of the user to authenticate.
    password: str
        The password of the user to authenticate.
    repo: AbstractRepository
        The repository object used to retrieve the user information.

    Raises:
    -------
    AuthenticationException
        If the user is not authenticated.

    """
    authenticated = False
    user = repo.get_user(username)
    if user:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    """

    Converts a User instance to a dictionary.

    :param user: A User object to be converted.
    :type user: User
    :return: A dictionary containing the username and password of the
    User object.
    :rtype: dict
    """
    user_dictionary = {'username': user.username, 'password': user.password}
    return user_dictionary

