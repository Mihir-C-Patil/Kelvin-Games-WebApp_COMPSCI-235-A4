import pytest
from flask import Flask
from flask.testing import FlaskClient

from games.authentication.services import NameNotUniqueException, UnknownUserException, AuthenticationException
from games.domainmodel.model import Game, Genre, User, Review
from games.gameLibrary.gameLibrary import games_by_genre, gameLibrary_blueprint
from games.gamesDescription import services as game_services
from games.gameLibrary import services as library_services
from games.homepage import services as home_services
from games.userProfile import services as user_services
from games.authentication import services as authentication_services


def test_get_game_by_id(in_memory_repo):
    # Test game description service layer retrieves correct game using id
    game = game_services.get_game(in_memory_repo, 7940)
    assert game == Game(7940, 'Call of Duty® 4: Modern Warfare®')


def test_get_similar_games(in_memory_repo):
    # Test game description service layer returning games with the same genre
    games = game_services.similar_game(in_memory_repo, [Genre('Action'), Genre('Adventure')])
    assert len(games) == 14


def test_get_all_games_for_slides(in_memory_repo):
    # This tests whether the library service layer is getting the games in a dictionary and the right games are being fetched
    games = library_services.get_slide_games(in_memory_repo)
    assert len(games) == 4
    assert type(games[1]) == dict
    assert games[1]['title'] == "Max Payne"
    assert games[1]['game_id'] == 12140
    assert games[2]['title'] == 'The Chaos Engine'


def test_get_games_by_genre(in_memory_repo):
    # Tests library service layer to check if it can return games by genre and checks to see if it is type dict
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


def test_can_add_reviews(in_memory_repo):
    # Tests to see if Review is added
    get_game = game_services.get_game(in_memory_repo, 7940)
    rating = 5
    review = "This is a great game!"
    user = User("Bob", "Hello123fr")
    add_review = game_services.add_review(rating, review, user, get_game)
    assert add_review == True


def test_can_user_add_two_reviews(in_memory_repo):
    # This test checks to see if a user can make review for a game twice
    get_game = game_services.get_game(in_memory_repo, 7940)
    rating = 3
    review = "This game is mid!"
    user = User("Bob", "Hello123fr")
    add_review1 = game_services.add_review(rating, review, user, get_game)
    rating2 = 5
    review2 = "This is a great game!"
    add_review = game_services.add_review(rating2, review2, user, get_game)
    assert add_review == False


def test_average_rating_when_no_reviews_exist(in_memory_repo):
    # Checks if the correct average is being returned when no ratings are present
    get_game = game_services.get_game(in_memory_repo, 1228870)
    average = game_services.get_average(get_game)
    assert average == 0.0


def test_average_rating_with_reviews(in_memory_repo):
    get_game = game_services.get_game(in_memory_repo, 7940)
    game_services.add_review(5, "This is excellent", User('Bill', 'Dfjhrfh34859832'), get_game)
    game_services.add_review(4, "This is excellent", User('Jack', 'Dfjhrfh34859832'), get_game)
    game_services.add_review(2, "This is excellent", User('Eden', 'Dfjhrfh34859832'), get_game)
    game_services.add_review(3, "This is excellent", User('Bob', 'Dfjhrfh34859832'), get_game)
    average = game_services.get_average(get_game)
    assert average == 3.5


def test_add_game_to_wishlist_valid():
    # Checks to see if a valid game is added to users wishlist
    user = User('Bill', 'Dfjhrfh34859832')
    game = Game(7940, 'Call of Duty® 4: Modern Warfare®')
    user_services.add_game_to_wishlist(user, game)
    assert len(user.get_wishlist().list_of_games()) == 1
    assert user.get_wishlist().list_of_games()[0] == game


def test_add_duplicate_game_to_wishlist():
    # test to see if a duplicate game can be added to the same wishlist
    user = User('Bill', 'Dfjhrfh34859832')
    game = Game(7940, 'Call of Duty® 4: Modern Warfare®')
    user_services.add_game_to_wishlist(user, game)
    user_services.add_game_to_wishlist(user, game)
    assert len(user.get_wishlist().list_of_games()) == 1
    assert user.get_wishlist().list_of_games()[0] == game


def test_remove_game_from_wishlist():
    user = User('Bill', 'Dfjhrfh34859832')
    game = Game(7940, 'Call of Duty® 4: Modern Warfare®')
    user_services.add_game_to_wishlist(user, game)
    game2 = Game(6748, 'Fifa 23')
    user_services.add_game_to_wishlist(user, game2)
    user_services.remove_game_from_wishlist(user, game2)
    assert user.get_wishlist().list_of_games()[0] == game
    assert len(user.get_wishlist().list_of_games()) == 1


def get_user_empty_wishlist():
    # Test to see if empty wishlist is returned
    user = User('Bill', 'Dfjhrfh34859832')
    user_wishlist = user_services.get_user_wishlist(user)
    assert len(user_wishlist) == 0
    assert isinstance(user_wishlist, list)


def test_user_with_games_in_wishlist():
    # Test to see if games were added in the wishlist and wishlist was returned correctly
    user = User('Bill', 'Dfjhrfh34859832')
    game = Game(7940, 'Call of Duty® 4: Modern Warfare®')
    game2 = Game(6748, 'Fifa 23')
    user_services.add_game_to_wishlist(user, game)
    user_services.add_game_to_wishlist(user, game2)
    wishlist = user_services.get_user_wishlist(user)
    assert len(wishlist) == 2
    assert isinstance(wishlist, list)


def test_user_added_successful(in_memory_repo):
    # This test determines if user is added to memory repository
    authentication_services.add_user('Bob', 'Dhrh3i3242', in_memory_repo)
    assert in_memory_repo.get_user('Bob') == User('Bob', 'Dhrh3i3242')


def test_add_user_with_duplicate_username(in_memory_repo):
    authentication_services.add_user('Bob', 'Dhrh3i3242', in_memory_repo)
    try:
        authentication_services.add_user('Bob', 'Hello123d', in_memory_repo)
        assert False
    except NameNotUniqueException:
        pass


def test_get_valid_user(in_memory_repo):
    # Test to get valid user from memory repository
    user = User('Bill', 'dhfsjk123D')
    authentication_services.add_user('Bill', 'dhfsjk123D', in_memory_repo)
    get_user = authentication_services.get_user('Bill', in_memory_repo)
    assert get_user == user


def test_get_invalid_user(in_memory_repo):
    # Test to check if invalid user was returned from memory repository
    authentication_services.add_user('Bill', 'dhfsjk123D', in_memory_repo)
    try:
        get_user = authentication_services.get_user('Sarah', in_memory_repo)
        assert False
    except UnknownUserException:
        pass


def test_verify_valid_user(in_memory_repo):
    # Test to check if valid user is autheticated
    authentication_services.add_user('Bill', 'dhfsjk123D', in_memory_repo)
    try:
        authentication_services.authenticate_user('Bill', 'dhfsjk123D', in_memory_repo)
    except AuthenticationException:
        assert False

def test_verify_invalid_username(in_memory_repo):
    # Test to check invalid username authentication
    authentication_services.add_user('Bill', 'dhfsjk123D', in_memory_repo)
    try:
        authentication_services.authenticate_user('Chris', 'dhfsjk123D', in_memory_repo)
        assert False
    except AuthenticationException:
        pass

def test_verify_invalid_password(in_memory_repo):
    # Test to check invalid password authentication
    authentication_services.add_user('Bill', 'dhfsjk123D', in_memory_repo)
    try:
        authentication_services.authenticate_user('Bill', 'WrongPassword', in_memory_repo)
        assert False
    except AuthenticationException:
        pass

def test_user_to_dict():
    user = User('Bill', 'dhfsjk123D')
    user_dict = authentication_services.user_to_dict(user)
    assert isinstance(user_dict, dict)
    assert 'username' in user_dict
    assert 'password' in user_dict
    assert user_dict['username'] == 'Bill'
    assert user_dict['password'] == 'dhfsjk123D'
