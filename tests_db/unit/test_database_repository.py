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
    education = Genre("Education")
    similar_games = repo.get_similar_games([education])
    assert len(similar_games) == 5

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

