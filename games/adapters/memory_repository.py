import os.path
from abc import ABC
from bisect import insort_left
from typing import List
from pathlib import Path
from games.domainmodel.model import *
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository


class MemoryRepository(AbstractRepository, ABC):
    """
    A memory-based repository implementation for games and genres.
    """

    def __init__(self, message=None):
        self.__games = list()
        self.__genres = list()
        self.__users = list()
        self.comments = list()
        self.__user_wishlist_games = list()
        self.__reviews = list()
        self.__publishers = list()

    def add_game(self, game: Game):
        """
        Add a game to the repository.

        Args:
            game (Game): The game to be added.
        """
        if isinstance(game, Game):
            insort_left(self.__games, game)

    def get_games(self) -> List[Game]:
        """
        Get a list of all games in the repository.

        Returns:
            List[Game]: A list of Game objects in the repository.
        """
        return self.__games

    def get_slide_games(self) -> List[Game]:
        """
        Get a list of games for sliding carousel display.

        Returns:
            List[Game]: A list of Game objects for the sliding carousel.
        """
        return self.__games

    def get_number_of_games(self):
        """
        Get the total number of games in the repository.

        Returns:
            int: The total number of games in the repository.
        """
        return len(self.__games)

    def get_games_by_id(self, game_id):
        """
        Args:
            game_id: The ID of the game to retrieve.

        Returns:
            The game with the specified ID, if found. If no game is
            found with the specified ID, None is returned.
        """
        for game in self.__games:
            if game.game_id == game_id:
                return game
        return None

    def get_similar_games(self, genre_list):
        """
        Args:
            genre_list (List[str]): A list of genres to search for
            similar games.

        Returns:
            List[Game]: A list of games that have at least one genre
            in common with the genre_list.
        """
        similar_game_list = []
        for game in self.__games:
            for genre in game.genres:
                if genre in genre_list:
                    similar_game_list.append(game)
                    break
        return similar_game_list

    def search_games_by_title(self, game_title: str) -> List[Game]:
        """
        Args:
            game_title: A string representing the title of the game to
            search for.

        Returns:
            A list of Game objects that match the given game_title.

        """
        game_title = game_title.lower()
        game_results = [game for game in self.__games if game_title
                        in game.title.lower()]
        return game_results

    def search_games_by_publisher(self, publisher: str) -> List[Game]:
        """
        Searches the games in the repository by publisher.

        Args:
            publisher (str): The name of the publisher to search for.

        Returns:
            List[Game]: A list of games that match the publisher.

        """
        publisher = publisher.lower()
        game_results = [game for game in self.__games if publisher
                        in game.publisher.publisher_name.lower()]
        return game_results

    def search_games_by_category(self, category: str) -> List[Game]:
        """
        Searches for games by category.

        Args:
            category: A string representing the category to search for.

        Returns:
            A list of Game objects that belong to the specified category.

        """
        category = category.lower()
        game_results = [game for game in self.__games if category
                        in [category.lower() for category in game.categories]]
        return game_results

    def search_games_by_tags(self, tags: str) -> List[Game]:
        """
        Searches for games based on provided tags.

        Args:
            tags (str): A string representing the tags to search for.

        Returns:
            List[Game]: A list of games that match the provided tags.
        """
        tags = tags.lower()
        game_results = [game for game in self.__games if tags
                        in [tag.lower() for tag in game.tags]]
        return game_results

    def add_genre(self, genre: Genre):
        """
        Args:
            genre: The genre to be added to the repository.

        """
        if isinstance(genre, Genre) and genre not in self.__genres:
            insort_left(self.__genres, genre)

    def get_genres(self) -> List[Genre]:
        """
        Get a list of all genres in the repository.

        Returns:
            List[Genre]: A list of all genres in the repository.
        """
        return self.__genres

    def get_genre_of_games(self, target_genre):
        """
        Args:
            target_genre: The genre of games to search for.

        Returns:
            List[Game]: A list of games that have the specified genre.

        """
        matching_game_genre = []
        for game in self.__games:
            if Genre(target_genre) in game.genres:
                matching_game_genre.append(game)
            else:
                pass

        return matching_game_genre

    def add_user(self, user: User) -> None:
        """
        Add a user to the repository.

        :param user:     The user object to add to the repository.
        :type user:      User
        :return:         None
        """
        self.__users.append(user)

    def get_user(self, username: str) -> (User, None):
        """
        Get a specific user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The user object with the specified username.

            None: If no user with the specified username exists.
        """
        return next((user for user in self.__users if user.username
                     == username.lower().strip()), None)

    def add_publisher(self, publisher) -> None:
        """
        Adds a publisher to the list of publishers in the repository.

        Args:
            publisher (Publisher): The publisher to be added.

        Returns:
            None
        """
        if publisher not in self.__publishers:
            self.__publishers.append(publisher)

    def get_publishers(self) -> list[Publisher]:
        """

            Returns a list of all publishers in the repository.

            Returns:
                list[Publisher]: A list of Publisher objects
                representing all publishers in the repository.

        """
        return self.__publishers


# def populate(data_path: Path, repo: AbstractRepository):
#     """
#     Populate the repository with data from a CSV file.
#
#     Args:
#         data_path (Path): The path to the data directory.
#         repo (AbstractRepository): The repository to populate.
#     """
#     directory_name = os.path.dirname(os.path.abspath(__file__))
#     games_csv_path = data_path / "games.csv"
#     reader = GameFileCSVReader(games_csv_path)
#
#     reader.read_csv_file()
#     games = reader.dataset_of_games
#     for game in games:
#         repo.add_game(game)
#         for genre in game.genres:
#             repo.add_genre(genre)
