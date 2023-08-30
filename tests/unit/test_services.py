import pytest
from games.domainmodel.model import Game, Genre
from games.gamesDescription import services as game_services
from games.gameLibrary import services as library_services
from games.homepage import services as home_services

def test_get_game_by_id(in_memory_repo):
    #Test game description service layer retrieves correct game using id
    game = game_services.get_game(in_memory_repo, 7940)
    assert game == Game(7940, 'Call of Duty® 4: Modern Warfare®')

def test_get_similar_games(in_memory_repo):
    #Test game description service layer returning games with the same genre
    games = game_services.similar_game(in_memory_repo, [Genre('Action'), Genre('Adventure')])
    assert len(games) == 14

def test_get_all_games_for_slides(in_memory_repo):
    #This tests whether the library service layer is getting the games in a dictionary and the right games are being fetched
    games = library_services.get_slide_games(in_memory_repo)
    assert len(games) == 4
    assert type(games[1]) == dict
    assert games[1]['title'] == "Max Payne"
    assert games[1]['game_id'] == 12140
    assert games[2]['title'] =='The Chaos Engine'

def test_get_games_by_genre(in_memory_repo):
    #Tests library service layer to check if it can return games by genre and checks to see if it is type dict
    games = library_services.get_games_by_genre('Action', in_memory_repo)
    assert len(games) == 14
    assert games[0]['game_id'] == 7940
    assert games[0]['title'] == 'Call of Duty® 4: Modern Warfare®'
    assert type(games[1]) == dict
    assert type(games[4]) == dict


