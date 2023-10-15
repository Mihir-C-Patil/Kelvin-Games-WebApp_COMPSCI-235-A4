# from typing import List
#
# from games import Publisher
from games.adapters.datareader.csvdatareader import *
from games.adapters.repository import AbstractRepository


class GameFileCSVReader:
    """
    Class GameFileCSVReader

    A class to read game data from a CSV file and populate a repository.

    Attributes:
        __filename (str): The path to the CSV file.
        __repo (AbstractRepository): The repository to populate.
        __database_mode (bool): A flag indicating whether the data
        should be stored in a database.
        __dataset_of_games (list[Game]): A list of game objects.
        __dataset_of_publishers (set): A set of publisher objects.
        __dataset_of_genres (set): A set of genre objects.
        __dataset_of_reviews (set): A set of review objects.
        __dataset_of_tags (set): A set of tag objects.
        __dataset_of_languages (set): A set of language strings.
        __dataset_of_categories (set): A set of category strings.

    Methods:
        read_csv_file(file=None): Read the CSV file and populate the
        repository with game data.
        dataset_of_games: Get the list of game objects.
        dataset_of_publishers: Get the list of unique publisher objects.
        dataset_of_genres: Get the list of unique genre objects.
    """
    def __init__(self, filename, repo: AbstractRepository, db_mode: bool):
        self.__filename = filename
        self.__repo = repo
        self.__database_mode = db_mode
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()
        self.__dataset_of_reviews = set()
        self.__dataset_of_tags = set()
        self.__dataset_of_languages = set()
        self.__dataset_of_categories = set()

    def read_csv_file(self, file=None):
        """
        Reads a CSV file containing game data and adds the games to the
        repository.

        Args:
            file (str): The path to the CSV file containing the game
            data.

        """
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    game_id = int(row["AppID"])
                    title = row["Name"]
                    game = Game(game_id, title)
                    game.release_date = row["Release date"]
                    game.price = float(row["Price"])
                    game.description = row["About the game"]
                    game.image_url = row["Header image"]
                    if len(row["Movies"]) > 0:
                        game.video_url = row["Movies"]

                    publisher = Publisher(row["Publishers"])
                    self.__repo.add_publisher(publisher)
                    game.publisher = publisher

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        genre = Genre(genre_name.strip())
                        self.__repo.add_genre(genre)
                        game.add_genre(genre)

                    languages = row["Supported languages"].split(",")
                    for language in languages:
                        new_language = language.strip().strip("[]'")
                        game.add_language(new_language)

                    if row["Windows"].lower() == "true":
                        game.system_dict["windows"] = True
                    else:
                        game.system_dict["windows"] = False

                    if row["Mac"].lower() == "true":
                        game.system_dict["mac"] = True
                    else:
                        game.system_dict["mac"] = False

                    if row["Linux"].lower() == "true":
                        game.system_dict["linux"] = True
                    else:
                        game.system_dict["linux"] = False

                    categories = row["Categories"].split(",")
                    for category in categories:
                        game.add_category(category.strip())

                    tags = row["Tags"].split(",")
                    for tag in tags:
                        game.add_tag(tag.strip())
                    self.__repo.add_game(game)


                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    @property
    def dataset_of_games(self) -> list[Game]:
        """

        Retrieves the dataset of games from the repository.

        Returns:
            list[Game]: A list of Game objects representing the dataset
            of games.

        """
        return self.__repo.get_games()

    @property
    def dataset_of_publishers(self) -> list[Publisher]:
        """
        Get a dataset of all publishers in the game file CSV reader.

        Returns:
            A list of Publisher objects representing all publishers in
            the game file.

        Example:
            reader = GameFileCSVReader()
            publishers = reader.dataset_of_publishers()
        """
        return list(set(self.__repo.get_publishers()))

    @property
    def dataset_of_genres(self) -> list[Genre]:
        """

        Returns a list of all genres in the dataset.

        :return: A list of Genre objects representing all genres in the
        dataset.
        :rtype: list[Genre]

        """
        return self.__repo.get_genres()
