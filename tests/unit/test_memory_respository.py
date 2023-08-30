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
    #Test to see if we can retrieve a game from repository using game id
    game = in_memory_repo.get_games_by_id(7940)
    assert game == Game(7940, 'Call of Duty® 4: Modern Warfare®')

def test_get_number_of_games(in_memory_repo):
    #Test to see how many games in repository
    assert in_memory_repo.get_number_of_games() == 14

def test_get_game(in_memory_repo):
    #Test to see if the get_games function is returning a list and whether the list has been populated
    assert type(in_memory_repo.get_games()) == list and len(in_memory_repo.get_games()) > 0

def test_get_games_by_invalid_id(in_memory_repo):
    #This tests checks what happens when we obtain a game using an id not in the repository
    game = in_memory_repo.get_games_by_id(34242)
    assert game == None

def test_get_games_by_similar_genre(in_memory_repo):
    #This test returns a list of similar games
    action = Genre("Action")
    adventure = Genre("Adventure")
    similar_games = in_memory_repo.get_similar_games([action, adventure])
    assert len(similar_games) == 14

def test_get_games_by_similar_genre_but_no_result(in_memory_repo):
    #This test also returns a list of similar games however there is no education genre in the sample set
    education = Genre("Education")
    similar_games = in_memory_repo.get_similar_games([education])
    assert len(similar_games) == 0

def test_search_games_by_title(in_memory_repo):
    #Test to check if we are able to search for a game using title
    game = in_memory_repo.search_games_by_title("Call of Duty® 4: Modern Warfare®")
    assert game == [Game(7940, 'Call of Duty® 4: Modern Warfare®')]

def test_search_games_by_publisher(in_memory_repo):
    #Test to check if we are able to search for a game using publisher name
    game = in_memory_repo.search_games_by_publisher("Buka Entertainment")
    assert game == [Game(311120,'Buka Entertainment')]

def test_search_games_by_category(in_memory_repo):
    #Test to check if we are able to search using categories
    game = in_memory_repo.search_games_by_category('VR Support')
    assert game == [Game(418650, 'Space Pirate Trainer')]

def test_search_games_by_category_to_return_all_games(in_memory_repo):
    #Uses a common category in the dataset to check if it returns a list with all games
    game = in_memory_repo.search_games_by_category('Single-player')
    assert len(game) == 14

def test_search_games_by_tags(in_memory_repo):
    #Test to check if we are able to search for a game using tags
    game = in_memory_repo.search_games_by_tags('Steampunk')
    assert game == [Game(242530,'The Chaos Engine'),Game(1228870,"Bartlow's Dread Machine")]

def test_number_unique_genres(in_memory_repo):
    #Test the number of unique genres in the dataset
    game = in_memory_repo.get_genres()
    assert len(game) == 1

def test_add_new_genre(in_memory_repo):
    #Test repository to add new genre and check if the count increases by 1
    old_size = len(in_memory_repo.get_genres())
    new_genre = Genre('Education')
    in_memory_repo.add_genre(new_genre)
    assert in_memory_repo.get_genres() == [Genre('Action'), Genre('Education')] and len(in_memory_repo.get_genres()) == old_size+1

def test_add_dupilicate_genre(in_memory_repo):
    #Test to see if a duplicate genre can be added to repository
    new_genre = Genre('Education')
    in_memory_repo.add_genre(new_genre)
    in_memory_repo.add_genre(Genre('Action'))
    assert in_memory_repo.get_genres() == [Genre('Action'), Genre('Education')]

def test_get_games_by_genre(in_memory_repo):
    #Test to get games based on genre
    game_list = in_memory_repo.get_genre_of_games('Action')
    assert len(game_list) == 14