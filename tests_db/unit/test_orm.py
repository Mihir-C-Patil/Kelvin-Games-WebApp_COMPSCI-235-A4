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

def insert_game_genre_association(empty_session, game_key, genre_key):
    sql = 'INSERT INTO game_genres(game_id, genre_name) VALUES (:game_id, :genre_name)'
    empty_session.execute(sql, {'game_id': game_key, 'genre_name': genre_key})

def make_game():
    game = Game(
        game_id=454680,
        game_title='MetaTron',
    )
    game.price = 0
    game.release_date = 'Dec 19, 2016'
    game.description = 'You are TRON!'

    # Create a Publisher object and set it for the game
    publisher = Publisher('TubbyKiD UG (haftungsbeschränkt)')
    game.publisher = publisher
    game.image_url = 'https://cdn.akamai.steamstatic.com/steam/apps/454680/ss_898bf6187d7a60a1cd59b728a9acca41cafeeebb.1920x1080.jpg?t=1545358112'

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

def make_user():
    user = User('Kelvin', 'Hello1234')
    return user

def make_review(user, game):
    review = Review(user, game, 5, 'This is a cool game')
    return review

def make_wishlist(user):
    wishlist = Wishlist(user)
    return wishlist

def test_loading_users(empty_session):
    # This test function inserts a user into the database and checks if the user was successfully inserted.
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
    # This test function inserts a game into the database and checks if the game was successfully inserted.
    game_key = insert_game(empty_session)
    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()
    assert fetched_game == expected_game

def test_review_games(empty_session):
    # This test function inserts a game review into the database and checks if the review is associated with the game.
    insert_game_review(empty_session)
    rows = empty_session.query(Game).all()
    game = rows[0]
    for review in game.reviews:
        assert type(review) == Review
        assert review.comment == 'Great Game'

def test_loading_of_genres(empty_session):
    # This test function inserts a genre into the database and checks if the genre was successfully inserted.
    genre = insert_genre(empty_session)
    expected_genre = make_genre()
    rows = empty_session.query(Genre).all()
    genre = rows[0]
    assert genre == expected_genre

def test_loading_publishers(empty_session):
    # This test function inserts a publisher into the database and checks if the publisher was successfully inserted.
    publisher = insert_publisher(empty_session)
    expected_pub = make_publisher()
    rows = empty_session.query(Publisher).all()
    publisher = rows[0]
    assert publisher == expected_pub
    assert type(publisher) == Publisher

def test_loading_of_genre_association_relationship(empty_session):
    # This test function inserts a game-genre association into the database and checks if the association is correct.
    game_key = insert_game(empty_session)
    genre_key = insert_genre(empty_session)
    insert_game_genre_association(empty_session, game_key, genre_key)
    game = empty_session.query(Game).get(game_key)
    genre = empty_session.query(Genre).get(genre_key)
    assert genre in game.genres

def test_user_persistence(empty_session):
    # This test function checks the persistence of a user in the database.
    user = make_user()
    empty_session.add(user)
    empty_session.commit()
    sql = 'SELECT username FROM user'
    get_user = empty_session.execute(sql).all()
    assert get_user == [('kelvin',)]

def test_user_persistence_password(empty_session):
    # This test function checks the persistence of a user's password in the database.
    user = make_user()
    empty_session.add(user)
    empty_session.commit()
    sql = 'SELECT username, password FROM user'
    get_user = empty_session.execute(sql).all()
    assert get_user == [('kelvin', 'Hello1234')]

def test_publisher_persistence(empty_session):
    # This test function checks the persistence of a publisher in the database.
    publisher = make_publisher()
    empty_session.add(publisher)
    empty_session.commit()
    sql = 'SELECT publisher_name FROM publisher'
    get_publisher = empty_session.execute(sql).all()
    assert get_publisher[0] == ('Kelvin Developers',)

def test_genre_persistence(empty_session):
    # This test function checks the persistence of a genre in the database.
    genre = make_genre()
    empty_session.add(genre)
    empty_session.commit()
    sql = 'SELECT genre_name FROM genre'
    get_genre = empty_session.execute(sql).all()
    assert get_genre[0] == ('Adventure',)

def test_game_persistence(empty_session):
    # This test function checks the persistence of a game in the database.
    game_object = make_game()
    empty_session.add(game_object)
    empty_session.commit()
    retrieved_game = empty_session.query(Game).filter(Game._Game__game_title == 'MetaTron').first()
    assert retrieved_game == game_object
    assert retrieved_game.price == game_object.price

def test_user_review_persistence(empty_session):
    # This test function checks the persistence of a user review in the database.
    user_object = make_user()
    game_object = make_game()
    empty_session.add(user_object)
    empty_session.add(game_object)
    create_review = make_review(user_object, game_object)
    empty_session.add(create_review)
    empty_session.commit()
    game_id = game_object.game_id
    retrieved_review = empty_session.query(Review).filter(Review._Review__game_id == game_id).first()
    assert retrieved_review == create_review
    assert retrieved_review.comment == create_review.comment

def insert_wishlist(empty_session):
    user = make_user()
    game = make_game()
    game_id = game.game_id
    wishlist_item = Wishlist(user)
    empty_session.add(wishlist_item)
    empty_session.commit()
    return wishlist_item.id

def test_insert_wishlist(empty_session):
    wishlist_id = insert_wishlist(empty_session)
    result = empty_session.execute('SELECT * FROM wishlist WHERE id = :wishlist_id',
                                   {'wishlist_id': wishlist_id}).fetchone()
    assert result is not None

def insert_game_and_publisher(empty_session):
    publisher = Publisher('Kelvin Developers')
    empty_session.add(publisher)
    empty_session.commit()
    game = Game(1, 'MetaTron')
    game.price=0
    game.release_date='Dec 19, 2016'
    game.description = 'You are TRON!'
    game.publisher = publisher
    game.image_url = 'test'
    empty_session.add(game)
    empty_session.commit()

def test_game_and_publisher_relationship(empty_session):
    # Test to check relationship between game and publisher is established
    insert_game_and_publisher(empty_session)
    game = empty_session.query(Game).filter(Game._Game__game_title == 'MetaTron').first()
    assert game.publisher.publisher_name == 'Kelvin Developers'

def test_user_wishlist_relationship(empty_session):
    # Tests for a one to one relationship
    user = make_user()
    wishlist = Wishlist(user)
    empty_session.add(user)
    empty_session.add(wishlist)
    empty_session.commit()
    get_user = empty_session.query(User).filter(User._User__username == 'kelvin').first()
    assert wishlist == get_user.get_wishlist()

def create_game():
    publisher = Publisher('Kelvin Developers')
    game = Game(1, 'MetaTron')
    game.price = 0
    game.release_date = 'Dec 19, 2016'
    game.description = 'You are TRON!'
    game.publisher = publisher
    game.image_url = 'test'
    return game

def test_user_review_relationship(empty_session):
    user1 = make_user()
    game = make_game()
    review1 = make_review(user1, game)
    empty_session.add(user1)
    empty_session.add(game)
    empty_session.commit()
    get_user_reviews = user1.reviews
    assert len(get_user_reviews) == 1
    assert review1.user == user1
