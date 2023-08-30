import csv
import os

from games.domainmodel.model import Genre, Game, Publisher


class GameFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()
        self.__dataset_of_reviews = set()
        self.__dataset_of_tags = set()
        self.__dataset_of_languages = set()
        self.__dataset_of_categories = set()

    def read_csv_file(self):
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
                    self.__dataset_of_publishers.add(publisher)
                    game.publisher = publisher

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        genre = Genre(genre_name.strip())
                        self.__dataset_of_genres.add(genre)
                        game.add_genre(genre)

                    game.reviews = row["Reviews"]

                    languages = row["Supported languages"].split(",")
                    for language in languages:
                        new_language = language.strip().strip("[]'")
                        self.__dataset_of_languages.add(new_language)
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
                        self.__dataset_of_categories.add(category.strip())

                    tags = row["Tags"].split(",")
                    for tag in tags:
                        game.add_tag(tag.strip())
                        self.__dataset_of_tags.add(tag.strip())

                    self.__dataset_of_games.append(game)


                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres
