import abc
from typing import List

from games.domainmodel.model import *

repo_instance = None


class RepositoryException(Exception):
    """
    An exception class for repository errors.
    """
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
    """AbstractRepository is an abstract base class that defines the
    interface for a repository to interact with the game library.

    Methods:
    - add_game(game: Game): Adds a game to the repository.
    - get_games() -> List[Game]: Returns a list of all games in the
      repository.
    - get_number_of_games(): Returns the number of games in the
      repository.
    - get_slide_games() -> List[Game]: Returns a list of games to be
      displayed on the home page slider.
    - add_genre(genre: Genre): Adds a genre to the repository.
    - get_genre_of_games(target_genre) -> List[Game]: Returns a list of
      games in the specified genre.
    - get_genres() -> List[Genre]: Returns a list of all genres in the
      repository.
    - get_games_by_id(game_id: int): Returns a game with the specified
      ID.
    - get_similar_games(genre): Returns a list of games similar to the
      specified genre.
    - search_games_by_title(game_title: str) -> List[Game]: Searches for
      games matching the given title.
    - search_games_by_publisher(query): Searches for games published by
      the specified publisher.
    - search_games_by_category(query): Searches for games in the
      specified category.
    - search_games_by_tags(query): Searches for games with the specified
      tags.
    - get_user(username: str) -> User: Returns a user with the specified
      username.
    - add_user(user: User) -> None: Adds a user to the repository.
    - get_all_reviews() -> None: Returns all reviews in the repository.
    - add_publisher(publisher) -> None: Adds a publisher to the
      repository.
    - get_publishers() -> List[Publisher]: Returns a list of all
      publishers.
    - get_tags() -> List[str]: Returns a list of all tags.
    - add_wish_game(user, game): Adds a game to the wishlist of the
      specified user.
    - remove_wish_game(user, game): Removes a game from the wishlist of
      the specified user.
    - get_wishlist(user): Returns the wishlist of the specified user.
    - add_review(user, game, rating, review): Adds a review for the
      specified game by the specified user.
    - get_user_review(user): Returns the reviews submitted by the
      specified user.

    This class is an abstract base class (ABC) that cannot be
    instantiated directly. Subclasses are expected to implement the
    abstract methods defined in this class.
    """
    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_slide_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre_of_games(self, target_genre) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_id(self, game_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_similar_games(self, genre):
        raise NotImplementedError

    def search_games_by_title(self, game_title: str) -> List[Game]:
        raise NotImplementedError

    def search_games_by_publisher(self, query):
        raise NotImplementedError

    def search_games_by_category(self, query):
        raise NotImplementedError

    def search_games_by_tags(self, query):
        raise NotImplementedError

    def get_user(self, username: str) -> User:
        raise NotImplementedError

    def add_user(self, user: User) -> None:
        raise NotImplementedError

    def get_all_reviews(self) -> None:
        raise NotImplementedError

    def add_publisher(self, publisher) -> None:
        raise NotImplementedError

    def get_publishers(self) -> list[Publisher]:
        raise NotImplementedError

    def get_tags(self) -> list[str]:
        raise NotImplementedError

    def add_wish_game(self, user, game):
        raise NotImplementedError

    def remove_wish_game(self, user, game):
        raise NotImplementedError

    def get_wishlist(self, user):
        raise NotImplementedError

    def add_review(self, user, game, rating, review):
        raise NotImplementedError

    def get_user_review(self, user):
        raise NotImplementedError
