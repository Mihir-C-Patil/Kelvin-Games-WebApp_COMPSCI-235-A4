from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Review, Game



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

def add_review(rating: int, review: str, user: User, game: Game):
    new_review = Review(user, game, rating, review)
    if len(game.reviews) == 0:
        user.add_review(new_review)
        game.add_review(new_review)
    else:
        for review in game.reviews:
            if user != review.user:
                user.add_review(new_review)
                game.add_review(new_review)

def get_average(game: Game):
    rating = 0
    average = 0
    for review in game.reviews:
        rating += review.rating
    if len(game.reviews) > 0:
        average = rating / len(game.reviews)
    return average

