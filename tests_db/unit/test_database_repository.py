import datetime

import pytest
from games.domainmodel.model import Game, User, Genre, Review, Wishlist, Publisher
from games.adapters.repository import RepositoryException
from games.adapters import database_repository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

def test_repository_can_add_a_user(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Kelvin', 'ABCDEF1234')
    user1 = User('Bob', 'Hello1234')
    repo.add_user(user)
    repo.add_user(user1)
    get_user = repo.get_user('kelvin')
    assert user == get_user and isinstance(get_user, User)

def test_number_of_games_in_database(session_factory):
    # Check if we can retreive the correct number of games in database
    repo = database_repository.SqlAlchemyRepository(session_factory)
    games = repo.get_games()
    assert len(games) == 981

def test_can_retrieve_game_by_id(session_factory):
    # Check if we can retreive game by id
    repo = database_repository.SqlAlchemyRepository(session_factory)
    game = repo.get_games_by_id(1228870)
    assert game == Game(1228870, "Bartlow's Dread Machine")

def test_get_genres(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    genre = repo.get_genres()
    assert type(genre) == list
    assert len(genre) == 26

def test_get_games_by_invalid_id(session_factory):
    #This tests checks what happens when we obtain a game using an id not in the repository
    repo = database_repository.SqlAlchemyRepository(session_factory)
    game = repo.get_games_by_id(34242)
    assert game == None

def test_get_games_by_similar_genre(session_factory):
    # This test returns a list of similar games
    repo = database_repository.SqlAlchemyRepository(session_factory)
    education = Genre("Action")
    similar_games = repo.get_similar_games([education])
    assert len(similar_games) == 0

def test_search_games_by_title(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    #Test to check if we are able to search for a game using title
    game = repo.search_games_by_title("Call of Duty® 4: Modern Warfare®")
    assert game == [Game(7940, 'Call of Duty® 4: Modern Warfare®')]

def test_search_games_by_publisher(session_factory):
    #Test to check if we are able to search for a game using publisher name
    repo = database_repository.SqlAlchemyRepository(session_factory)
    game = repo.search_games_by_publisher("Buka Entertainment")
    assert len(game) == 2

def test_get_games_by_genre(session_factory):
    #Test to get games based on genre
    repo = database_repository.SqlAlchemyRepository(session_factory)
    game_list = repo.get_genre_of_games('Education')
    assert len(game_list) == 5

def test_get_genres(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    genre_list = repo.get_genres()
    assert len(genre_list) == 26


def test_get_game_by_genre(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    games = repo.get_genre_of_games('Action')
    game = Game(7940, 'Call of Duty® 4: Modern Warfare®')
    assert len(games) == 405
    assert game in games

def test_get_game_by_invalid_genre(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    invalid_games = repo.get_genre_of_games('invalid')
    assert len(invalid_games) == 0

def test_slide_games(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    games = repo.get_slide_games()
    game = Game(7940, 'Call of Duty® 4: Modern Warfare®')
    assert game in games

def test_search_games_by_invalid_tags(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    games_by_tag = repo.search_games_by_tags('invalid')
    assert len(games_by_tag) == 0

def test_get_game_by_invalid_id(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    invalid_game = repo.get_games_by_id(4)
    assert invalid_game == None

def test_add_to_wishlist(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Kelvin', 'ABCDEF1234')
    user1 = User('Bob', 'Hello1234')
    repo.add_user(user)
    repo.add_user(user1)
    get_user = repo.get_user('kelvin')
    game2 = Game(1, 'Spongebob')
    game3 = Game(2, 'Fifa')
    repo.add_wish_game(user, game2)
    wishlist = repo.get_wishlist(user)
    assert user == get_user and isinstance(get_user, User)

def test_user_wishlist_empty(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Kelvin', 'ABCDEF1234')
    repo.add_user(user)
    get_wishlist = repo.get_wishlist(user)
    assert get_wishlist == []

def test_search_games_by_invalid_title(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    games = repo.search_games_by_title('NonExistentGame')
    assert len(games) == 0

def test_add_to_wishlist(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Kelvin', 'password123')
    game = repo.get_games_by_id(7940)
    repo.add_user(user)
    repo.add_game(game)
    repo.add_wish_game(user, game)
    wishlist = repo.get_wishlist(user)
    assert game in wishlist
    assert len(wishlist) == 1

def test_remove_games_from_wishlist(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Kelvin', 'password123')
    game = repo.get_games_by_id(7940)
    repo.add_user(user)
    repo.add_game(game)
    repo.add_wish_game(user, game)
    game2 = repo.get_games_by_id(311120)
    game3 = repo.get_games_by_id(418650)
    repo.add_wish_game(user, game2)
    repo.add_wish_game(user, game3)
    wishlist = repo.get_wishlist(user)
    repo.remove_wish_game(user, game2)
    assert game2 not in wishlist

def test_user_can_add_review(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Kelvin', 'password123')
    repo.add_user(user)
    game = repo.get_games_by_id(7940)
    repo.add_review(user, game, 5, 'Cool Game')
    get_review = repo.get_user_review(user)
    assert len(get_review) == 1

def test_get_user_review(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Kelvin', 'password123')
    repo.add_user(user)
    game = repo.get_games_by_id(7940)
    repo.add_review(user, game, 5, 'Cool Game')
    get_review = repo.get_user_review(user)
    assert type(get_review[0]) == Review

def test_user_can_add_multiple_review(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    user = User('Kelvin', 'password123')
    repo.add_user(user)
    game = repo.get_games_by_id(7940)
    repo.add_review(user, game, 5, 'Cool Game')
    game_1 = repo.get_games_by_id(311120)
    repo.add_review(user, game_1, 4, 'Great!')
    get_review = repo.get_user_review(user)
    assert len(get_review) == 2

def add_game(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    game = Game(1, 'spongebob')
    game.price = 100.01
    game.release_date = datetime.datetime
    repo.add_game(game)
    assert repo.get_number_of_games() == 982

def add_multiple_games(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    game = Game(1, 'spongebob')
    game.price = 100.01
    game.release_date = datetime.datetime
    game2 = Game(2, 'fifa')
    game2.price = 100.01
    game2.release_date = datetime.datetime
    game3 = Game(3, 'NBA')
    game.price = 100.01
    game.release_date = datetime.datetime
    repo.add_game(game)
    assert repo.get_number_of_games() == 985

def test_add_genre(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    genre = Genre('new_genre')
    repo.add_genre(genre)
    assert genre in repo.get_genres()

def test_add_multiple_genres(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    genre = Genre('new_genre')
    genre1 = Genre('new_genre1')
    genre2 = Genre('new_genre2')
    genre3 = Genre('new_genre3')
    repo.add_genre(genre)
    repo.add_genre(genre1)
    repo.add_genre(genre2)
    repo.add_genre(genre3)
    assert genre in repo.get_genres()
    assert genre1 in repo.get_genres()
    assert genre2 in repo.get_genres()
    assert genre3 in repo.get_genres()

def test_add_publisher(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    publisher = Publisher('Kelvin Developers')
    repo.add_publisher(publisher)
    assert publisher in repo.get_publishers()

def test_add_multiple_publisher(session_factory):
    repo = database_repository.SqlAlchemyRepository(session_factory)
    publisher_names = ['Hello', 'codemasters', 'ea sports']
    for name in publisher_names:
        repo.add_publisher(Publisher(name))
    assert Publisher('codemasters') in repo.get_publishers()