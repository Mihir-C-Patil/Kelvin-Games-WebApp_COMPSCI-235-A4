from games.adapters.repository import AbstractRepository


def get_game(repo: AbstractRepository, id):
    """

    :param repo: AbstractRepository object representing the repository
    that stores game information.
    :param id: The unique identifier of the game.

    :return: The game object with the specified id if found, otherwise
    None.

    """
    return repo.get_games_by_id(id)


def similar_game(repo: AbstractRepository, genre):
    """
    Get a list of similar games based on the specified genre.

    Parameters:
    repo (AbstractRepository): The repository object that contains game
    data.
    genre (str): The genre of the game.

    Returns:
    List: A list of similar games based on the specified genre.

    """
    return repo.get_similar_games(genre)
