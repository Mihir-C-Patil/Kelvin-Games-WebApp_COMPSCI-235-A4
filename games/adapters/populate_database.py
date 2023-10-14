# from typing import List
#
# from games import Publisher
from games.adapters.datareader.csvdatareader import *
from games.adapters.repository import AbstractRepository


class GameFileCSVReader:
    def __init__(self, filename, repo: AbstractRepository, database_mode: bool):
        self.__filename = filename
        self.__repo = repo
        self.__database_mode = database_mode
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()
        self.__dataset_of_reviews = set()
        self.__dataset_of_tags = set()
        self.__dataset_of_languages = set()
        self.__dataset_of_categories = set()

    def read_csv_file(self, file=None):
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
        return self.__repo.get_games()

    @property
    def dataset_of_publishers(self) -> list[Publisher]:
        return list(set(self.__repo.get_publishers()))

    @property
    def dataset_of_genres(self) -> list[Genre]:
        return self.__repo.get_genres()
