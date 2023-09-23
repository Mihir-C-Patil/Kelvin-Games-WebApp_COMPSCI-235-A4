from werkzeug.security import generate_password_hash, check_password_hash

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user:
        raise NameNotUniqueException

    password_hash = generate_password_hash(password)
    repo.add_user(User(username, password_hash))


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    authenticated = False
    user = repo.get_user(username)
    if user:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    user_dictionary = {'username': user.username, 'password': user.password}
    return user_dictionary

