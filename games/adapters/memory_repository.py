import os.path
from bisect import insort_left
from typing import List

from games.domainmodel.model import Game, Genre
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository


class MemoryRepository(AbstractRepository):
    def __init__(self, message=None):
        self.__games = list()
        self.__genres = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_slide_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre) and genre not in self.__genres:
            insort_left(self.__genres, genre)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def get_genre_of_games(self, target_genre):
        matching_game_genre = []
        for game in self.__games:
            if Genre(target_genre) in game.genres:
                matching_game_genre.append(game)
            else:
                # matching_game_genre.append(Game(786, " ".join(game.genres)))
                pass

        return matching_game_genre


def populate(repo: AbstractRepository):
    directory_name = os.path.dirname(os.path.abspath(__file__))
    games_csv_path = os.path.join(directory_name, "data/games.csv")
    reader = GameFileCSVReader(games_csv_path)

    reader.read_csv_file()
    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)
        for genre in game.genres:
            repo.add_genre(genre)
