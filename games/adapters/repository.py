import abc
from typing import List

from games.domainmodel.model import *

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
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

