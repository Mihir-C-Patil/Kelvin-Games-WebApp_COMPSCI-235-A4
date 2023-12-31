from games.adapters.repository import AbstractRepository


def add_game_to_wishlist(user, game, repo: AbstractRepository):
    """
    Add a game to the user's wishlist.

    Args:
        repo:
        user (User): The user for whom to add the game.
        game (Game): The game to be added to the wishlist.
    """
    # user.get_wishlist().add_wish_game(game)
    repo.add_wish_game(user, game)


def remove_game_from_wishlist(user, game, repo: AbstractRepository):
    """
    Remove a game from the user's wishlist.

    Args:
        repo:
        user (User): The user for whom to remove the game.
        game (Game): The game to be removed from the wishlist.
    """
    # user.get_wishlist().remove_game(game)
    repo.remove_wish_game(user, game)


def get_user_wishlist(user, repo: AbstractRepository):
    """
    Get the user's wishlist.

    Args:
        repo:
        user (User): The user for whom to retrieve the wishlist.

    Returns:
        list[Game]: A list of games in the user's wishlist.
    """
    # wishlist_games = user.get_wishlist().list_of_games()
    wishlist_games = repo.get_wishlist(user)
    wishlist_games_dicts = []
    print(wishlist_games)
    for game in wishlist_games:
        games_wishlist_games_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'game_url': game.website_url,
            'header_image': game.image_url,
            'price': game.price,
            'description': game.description,
            'release_date': game.release_date
        }
        wishlist_games_dicts.append(games_wishlist_games_dict)
    return wishlist_games_dicts


def get_user_wishlist_objs(user):
    wishlist_games = user.get_wishlist().list_of_games()
    return wishlist_games


def get_user_reviews(user, repo: AbstractRepository):
    return repo.get_user_review(user)

