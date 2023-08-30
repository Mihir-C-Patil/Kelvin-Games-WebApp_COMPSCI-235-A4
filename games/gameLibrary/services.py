from games.adapters.repository import AbstractRepository


def get_number_of_games(repo: AbstractRepository):
    """
    Get the total number of games in the repository.

    Args: repo (AbstractRepository): The repository instance to retrieve
    data from.

    Returns:
        int: The total number of games in the repository.
    """
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    """
    Get a list of dictionaries representing game information from the
    repository.

    Args: repo (AbstractRepository): The repository instance to retrieve
    data from.

    Returns: list: A list of dictionaries, each containing game information
    including game_id, title, game_url, header_image, price, description,
    and release_date.
    """
    games = repo.get_games()
    games_dictionaries = []
    for game in games:
        games_dictionary = {
            'game_id': game.game_id,
            'title': game.title,
            'game_url': game.website_url,
            'header_image': game.image_url,
            'price': game.price,
            'description': game.description,
            'release_date': game.release_date
        }
        games_dictionaries.append(games_dictionary)
    return games_dictionaries


def get_slide_games(repo: AbstractRepository):
    """
    Get a list of dictionaries representing game information for sliding
    carousel display.

    Args: repo (AbstractRepository): The repository instance to retrieve
    data from.

    Returns: list: A list of dictionaries, each containing game information
    for sliding carousel display.
    """
    games = repo.get_games()
    games_dictionaries = []
    i = 0
    for game in games:
        if i < 4:
            games_dict = {
                'game_id': game.game_id,
                'title': game.title,
                'game_url': game.website_url,
                'header_image': game.image_url,
                'price': game.price,
                'description': game.description,
                'release_date': game.release_date
            }
            games_dictionaries.append(games_dict)
            i += 1
        else:
            break
    return games_dictionaries


def get_games_by_genre(genre, repo: AbstractRepository):
    """
    Get a list of dictionaries representing game information filtered by a
    specific genre.

    Args: genre (str): The target genre for filtering. repo (
    AbstractRepository): The repository instance to retrieve data from.

    Returns: list: A list of dictionaries, each containing game information
    for the specified genre.
    """
    games = repo.get_genre_of_games(target_genre=genre)
    games_dicts = []
    for game in games:
        games_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'game_url': game.website_url,
            'header_image': game.image_url,
            'price': game.price,
            'description': game.description,
            'release_date': game.release_date
        }
        games_dicts.append(games_dict)
    return games_dicts


def get_genres(repo: AbstractRepository):
    """
    Get a list of available genres from the repository.

    Args:
        repo (AbstractRepository): The repository instance to retrieve data
        from.

    Returns:
        list: A list of available genres.
    """
    genres = repo.get_genres()
    return [genre.genre_name for genre in genres]
