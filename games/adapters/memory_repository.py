import os.path
from bisect import insort_left
from typing import List
from pathlib import Path
from games.domainmodel.model import *
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository


class MemoryRepository(AbstractRepository):
    """
    A memory-based repository implementation for games and genres.
    """

    def __init__(self, message=None):
        self.__games = list()
        self.__genres = list()

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

    # Other methods are similar in structure with appropriate explanations


def populate(data_path: Path, repo: AbstractRepository):
    """
    Populate the repository with data from a CSV file.

    Args:
        data_path (Path): The path to the data directory.
        repo (AbstractRepository): The repository to populate.
    """
    directory_name = os.path.dirname(os.path.abspath(__file__))
    games_csv_path = data_path / "games.csv"
    reader = GameFileCSVReader(games_csv_path)

    reader.read_csv_file()
    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)
        for genre in game.genres:
            repo.add_genre(genre)
