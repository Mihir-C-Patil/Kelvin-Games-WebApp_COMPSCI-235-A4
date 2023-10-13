import pytest
from sqlalchemy.exc import IntegrityError
from games.domainmodel.model import Game, User, Review, Genre, Wishlist

def insert_user(empty_session, values = None):
    new_name = 'Kelvin'
    password = 'Abcdef1234'
    if values is not None:
        new_name = values[0]
        password = values[1]

    empty_session.execute('INSERT INTO user (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': password})

    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]