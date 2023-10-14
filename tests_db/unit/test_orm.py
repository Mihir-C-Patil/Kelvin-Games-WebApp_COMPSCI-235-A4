import pytest
from sqlalchemy.exc import IntegrityError
from games.domainmodel.model import Game, User, Review, Genre, Wishlist, Publisher
import datetime

def insert_user(empty_session, values = None):
    new_name = 'Kelvin'
    password = 'Abcdef1234'
    if values is not None:
        new_name = values[0]
        password = values[1]

    empty_session.execute('INSERT INTO user (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': password})

    row = empty_session.execute('SELECT id from user where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO user (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from user'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_game(empty_session):
    sql = "INSERT INTO game (id, game_title, price, release_date, description, publisher, image_url, tags) VALUES (:id, :game_title, :price, :release_date, :description, :publisher, :image_url, :tags)"
    params = {
        'id': 454680,
        'game_title': 'MetaTron',
        'price': 0,
        'release_date': 'Dec 19, 2016',
        'description': 'You are TRON!',
        'publisher': 'TubbyKiD UG (haftungsbeschränkt)',
        'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/454680/ss_898bf6187d7a60a1cd59b728a9acca41cafeeebb.1920x1080.jpg?t=1545358112',
        'tags': 'Action'
    }
    empty_session.execute(sql, params)
    row = empty_session.execute('SELECT id FROM game WHERE id = 454680').fetchone()
    return row[0]

def insert_game_review(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)
    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    empty_session.execute(
        'INSERT INTO review (user, game, rating, comment, timestamp) VALUES '
        '(:user_id, :game_id, 5, "Great Game", :timestamp_1)',
        {'user_id': user_key, 'game_id': game_key, 'timestamp_1': timestamp_1}
    )
    row = empty_session.execute('SELECT id from game').fetchone()
    return row[0]

def insert_publisher(empty_session):
    name = 'Kelvin Developers'
    empty_session.execute(
        'INSERT INTO publisher (publisher_name) VALUES '
            '(:publisher_name)',
    {'publisher_name': name}
    )
    row = empty_session.execute('SELECT publisher_name from publisher WHERE publisher_name = "Kelvin Developers"').fetchone()
    return row[0]


def make_game():
    game = Game(454680, 'MetaTron')
    return game

def make_genre():
    genre = Genre("Adventure")
    return genre

def make_publisher():
    pub = Publisher('Kelvin Developers')
    return pub

def insert_genre(empty_session):
    empty_session.execute('INSERT INTO genre(genre_name) VALUES ("Adventure")')
    row = empty_session.execute('SELECT genre_name FROM genre where genre_name = "Adventure"').fetchone()
    return row[0]


def test_loading_users(empty_session):
    users = list()
    users.append(("andrew", "ABCDE1223"))
    users.append(("cindy", "ABCDE1223"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "ABCDE1223"),
        User("cindy", "ABCDE1223")
    ]
    assert empty_session.query(User).all() == expected

def test_loading_game(empty_session):
    game_key = insert_game(empty_session)
    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()
    assert fetched_game == expected_game

def test_review_games(empty_session):
    insert_game_review(empty_session)
    rows = empty_session.query(Game).all()
    game = rows[0]
    for review in game.reviews:
        assert type(review) == Review
        assert review.comment == 'Great Game'

def test_loading_of_genres(empty_session):
    genre = insert_genre(empty_session)
    expected_genre = make_genre()
    rows = empty_session.query(Genre).all()
    genre = rows[0]
    assert genre == expected_genre

def test_loading_publishers(empty_session):
    publisher = insert_publisher(empty_session)
    expected_pub = make_publisher()
    rows = empty_session.query(Publisher).all()
    publisher = rows[0]
    assert publisher == expected_pub
    assert type(publisher) == Publisher

def test_persistence_review(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)
    rows = empty_session.query(Game).all()
