import pytest
from games.domainmodel.model import Game, Genre
from games.adapters.repository import AbstractRepository
from games.adapters.repository import RepositoryException

def test_repository_can_add_game(in_memory_repo):
    # Test repository can add a game object
    game = Game(54757, 'Fifa 23')
    game_1 = Game(7940, 'Call of Duty® 4: Modern Warfare®')
    in_memory_repo.add_game(game)
    in_memory_repo.add_game(game_1)
    assert game in in_memory_repo.get_games()

def test_repository_can_retrieve_game_by_id(in_memory_repo):
    game = in_memory_repo.get_games_by_id(7940)
    print(game)
    assert game == Game(7940, 'Call of Duty® 4: Modern Warfare®')

def test_get_number_of_games(in_memory_repo):
    assert in_memory_repo.get_number_of_games() == 14

def test_get_game(in_memory_repo):
    assert type(in_memory_repo.get_games()) == list and len(in_memory_repo.get_games()) > 0

def test_get_games_by_invalid_id(in_memory_repo):
    game = in_memory_repo.get_games_by_id(34242)
    assert game == None

def test_get_games_by_similar_genre(in_memory_repo):
    action = Genre("Action")
    adventure = Genre("Adventure")
    similar_games = in_memory_repo.get_similar_games([action, adventure])
    assert len(similar_games) == 14

def test_get_games_by_similar_genre_but_no_result(in_memory_repo):
    education = Genre("Education")
    similar_games = in_memory_repo.get_similar_games([education])
    assert len(similar_games) == 0