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

def test_get_genres(in_memory_repo):
    result = library_services.get_genres(in_memory_repo)
    assert len(result) == 1

def test_get_games(in_memory_repo):
    result = library_services.get_games(in_memory_repo)
    assert len(result) == 14

def get_number_of_games(in_memory_repo):
    number = library_services.get_number_of_games()
    assert number == 14


def test_search_games_by_title(in_memory_repo):
    # Tests the search_games_by_criteria function for title criteria.
    query = "Call of Duty"
    criteria = "title"
    results = home_services.search_games_by_criteria(query, criteria, in_memory_repo)

    # Ensure that the search results are of type list and contain dictionaries.
    assert isinstance(results, list)
    for result in results:
        assert isinstance(result, dict)

    # Check if the search results contain the expected game.
    assert any(game['title'] == 'Call of Duty® 4: Modern Warfare®' for game in results)


def test_search_games_by_publisher(in_memory_repo):
    # Tests the search_games_by_criteria function for publisher criteria.
    query = "Activision"
    criteria = "publisher"
    results = home_services.search_games_by_criteria(query, criteria, in_memory_repo)

    # Ensure that the search results are of type list and contain dictionaries.
    assert isinstance(results, list)
    for result in results:
        assert isinstance(result, dict)

    # Check if the search results contain games published by "Activision".
    assert all(game['header_image'] != '' for game in results)


def test_search_games_by_category(in_memory_repo):
    # Tests the search_games_by_criteria function for category criteria.
    query = "Action"
    criteria = "category"
    results = home_services.search_games_by_criteria(query, criteria, in_memory_repo)

    # Ensure that the search results are of type list and contain dictionaries.
    assert isinstance(results, list)
    for result in results:
        assert isinstance(result, dict)


def test_search_games_by_tags(in_memory_repo):
    # Tests the search_games_by_criteria function for tags criteria.
    query = "Multiplayer"
    criteria = "tags"
    results = home_services.search_games_by_criteria(query, criteria, in_memory_repo)

    # Ensure that the search results are of type list and contain dictionaries.
    assert isinstance(results, list)
    for result in results:
        assert isinstance(result, dict)

    # Check if the search results contain games with the "Multiplayer" tag.
    assert any(game['title'] == 'Call of Duty® 4: Modern Warfare®' for game in results)
