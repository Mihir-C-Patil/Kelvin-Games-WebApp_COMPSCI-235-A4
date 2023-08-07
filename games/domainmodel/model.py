from datetime import datetime


class Publisher:
    def __init__(self, publisher_name: str) -> None:
        """
        Initialise the Publisher object.

        Parameters
        ----------
        publisher_name: str
            The name of the publisher. (set to None if invalid)

        :param publisher_name: str
        """

        if not isinstance(publisher_name, str) or not publisher_name.strip():
            self.__publisher_name = None
        else:
            self.__publisher_name = publisher_name.strip()

    def __repr__(self) -> str:
        """
        Return the representation of the Publisher object.

        :return: str
        """

        return f"<Publisher {self.__publisher_name}>"

    def __eq__(self, other) -> bool:
        """
        Return True if the Publisher object is equal to the other
        Publisher object.

        Parameters
        ----------
        other: Publisher
            The other Publisher object to check for equality with.

        :param other: Publisher
        :return: bool
        """

        if not isinstance(other, self.__class__):
            return False
        return self.__publisher_name == other.publisher_name

    def __lt__(self, other) -> bool:
        """
        Return True if the Publisher object is less than the other
        Publisher object. The comparison is based on the publisher name.

        Parameters
        ----------
        other: Publisher
            The other Publisher object to compare with.

        :param other: Publisher
        :return: bool
        """

        if not isinstance(other, self.__class__):
            return False
        return self.__publisher_name < other.__publisher_name

    def __hash__(self) -> int:
        """
        Returns the hash value of the Publisher object based on the
        publisher name.

        :return: int
        """
        return hash(self.__publisher_name)

    @property
    def publisher_name(self) -> str:
        """
        Return the name of the publisher.

        :return: str
        """

        return self.__publisher_name

    @publisher_name.setter
    def publisher_name(self, new_publisher_name: str) -> None:
        """
        Change the name of the publisher to the specified publisher.

        Parameters
        ----------
        new_publisher_name: str
            The new name of the publisher.

        :param new_publisher_name:
        :return: None
        """

        if isinstance(new_publisher_name, str) and new_publisher_name.strip():
            self.__publisher_name = new_publisher_name.strip()
        else:
            self.__publisher_name = None


class Genre:
    def __init__(self, genre_name: str) -> None:
        """
        Initialise the Genre object.

        Parameters
        ----------
        genre_name: str
            The name of the genre. (set to None if invalid)

        :param genre_name: str
        """

        if not isinstance(genre_name, str) or not genre_name.strip():
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    def __repr__(self) -> str:
        """
        Return the representation of the Genre object.

        :return: str
        """

        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other) -> bool:
        """
        Return True if the Genre object is equal to the other
        Genre object.

        Parameters
        ----------
        other: Genre
            The other Genre object to check for equality with.

        :param other: Genre
        :return: bool
        """

        if not isinstance(other, self.__class__):
            return False
        return self.__genre_name == other.genre_name

    def __lt__(self, other):
        """
        Return True if the Genre object is less than the other
        Genre object. The comparison is based on the publisher name.

        Parameters
        ----------
        other: Genre
            The other Genre object to compare with.

        :param other: Genre
        :return: bool
        """

        if not isinstance(other, self.__class__):
            return False
        return self.__genre_name < other.genre_name

    def __hash__(self) -> int:
        """
        Returns the hash value of the Genre object based on the
        genre name.

        :return: int
        """
        return hash(self.__genre_name)

    @property
    def genre_name(self) -> str:
        """
        Return the name of the publisher.

        :return: str
        """
        return self.__genre_name


class Game:
    def __init__(self, game_id: int, game_title: str) -> None:
        """
        Initialise a Game object

        Parameters
        ----------
        game_id: int
            The unique id of a game, must be a non-negative integer

        game_title: str
            The title of the game, must be a non-empty string


        :param game_id: int
        :param game_title: str
        :return None
        :raise ValueError
        """

        if not isinstance(game_id, int) or game_id < 0:
            raise ValueError("Game ID must be a non-negative integer.")
        self.__game_id = game_id

        if not isinstance(game_title, str) or not game_title.strip():
            self.__game_title = None
        else:
            self.__game_title = game_title.strip()

        self.__genres = list()
        self.__reviews = list()
        self.__price = None
        self.__release_date = None
        self.__description = None
        self.__publisher = None
        self.__image_url = None
        self.__website_url = None

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    @property
    def game_id(self):
        return self.__game_id

    @property
    def title(self):
        return self.__game_title

    @title.setter
    def title(self, new_title):
        if type(new_title) is str and new_title.strip() != "":
            self.__game_title = new_title.strip()
        else:
            self.__game_title = None

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price: float):
        if isinstance(price, (int, float)) and price >= 0:
            self.__price = price
        else:
            raise ValueError("Price must be a positive number!")

    @property
    def release_date(self):
        return self.__release_date

    @release_date.setter
    def release_date(self, release_date: str):
        if isinstance(release_date, str):
            try:
                # Check if the release_date string is in the correct date format (e.g., "Oct 21, 2008")
                datetime.strptime(release_date, "%b %d, %Y")
                self.__release_date = release_date
            except ValueError:
                raise ValueError("Release date must be in 'Oct 21, 2008' format!")
        else:
            raise ValueError("Release date must be a string in 'Oct 21, 2008' format!")

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str) and description.strip() != "":
            self.__description = description
        else:
            self.__description = None

    @property
    def image_url(self):
        return self.__image_url

    @image_url.setter
    def image_url(self, image_url: str):
        if isinstance(image_url, str) and image_url.strip() != "":
            self.__image_url = image_url
        else:
            self.__image_url = None

    @property
    def website_url(self):
        return self.__website_url

    @website_url.setter
    def website_url(self, website_url: str):
        if isinstance(website_url, str) and website_url.strip() != "":
            self.__website_url = website_url
        else:
            self.__website_url = None

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre) or genre in self.__genres:
            return
        self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return
        try:
            self.__genres.remove(genre)
        except ValueError:
            print(f"Could not find {genre} in list of genres.")
            pass

    def __repr__(self):
        return f"<Game {self.__game_id}, {self.__game_title}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__game_id == other.__game_id

    def __hash__(self):
        return hash(self.__game_id)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__game_id < other.game_id


class User:
    def __init__(self, username: str, password: str):
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError('Username cannot be empty or non-string!')
        else:
            self.__username = username.lower().strip()

        if isinstance(password, str) and len(password) >= 7:
            self.__password = password
        else:
            raise ValueError('Password not valid!')

        self.__reviews: list[Review] = []
        self.__favourite_games: list[Game] = []

    @property
    def username(self):
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def reviews(self) -> list:
        return self.__reviews

    def add_review(self, new_review):
        if not isinstance(new_review, Review) or new_review in self.__reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review):
        if not isinstance(review, Review) or review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def favourite_games(self) -> list:
        return self.__favourite_games

    def add_favourite_game(self, game):
        if not isinstance(game, Game) or game in self.__favourite_games:
            return
        self.__favourite_games.append(game)

    def remove_favourite_game(self, game):
        if not isinstance(game, Game) or game not in self.__favourite_games:
            return
        self.__favourite_games.remove(game)

    def __repr__(self):
        return f"<User {self.__username}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username == other.username

    def __hash__(self):
        return hash(self.__username)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username < other.username


class Review:
    def __init__(self, user: User, game: Game, rating: int, comment: str):

        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user

        if not isinstance(game, Game):
            raise ValueError("Game must be an instance of Game class")
        self.__game = game

        if not isinstance(rating, int) or not 0 <= rating <= 5:
            raise ValueError("Rating must be an integer between 0 and 5")
        self.__rating = rating

        if not isinstance(comment, str):
            raise ValueError("Comment must be a string")
        self.__comment = comment.strip()

    @property
    def game(self) -> Game:
        return self.__game

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def user(self) -> User:
        return self.__user

    @comment.setter
    def comment(self, new_text):
        if isinstance(new_text, str):
            self.__comment = new_text.strip()
        else:
            raise ValueError("New comment must be a string")

    @rating.setter
    def rating(self, new_rating: int):
        if isinstance(new_rating, int) and 0 <= new_rating <= 5:
            self.__rating = new_rating
        else:
            raise ValueError("Rating must be an integer between 0 and 5")

    def __repr__(self):
        return f"Review(User: {self.__user}, Game: {self.__game}, " \
               f"Rating: {self.__rating}, Comment: {self.__comment})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user == self.__user and other.game == self.__game and other.comment == self.__comment


class Wishlist:
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user

        self.__list_of_games = []

    def list_of_games(self):
        return self.__list_of_games

    def size(self):
        size_wishlist = len(self.__list_of_games)
        if size_wishlist > 0:
            return size_wishlist

    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.__list_of_games:
            self.__list_of_games.append(game)

    def first_game_in_list(self):
        if len(self.__list_of_games) > 0:
            return self.__list_of_games[0]
        else:
            return None

    def remove_game(self, game):
        if isinstance(game, Game) and game in self.__list_of_games:
            self.__list_of_games.remove(game)

    def select_game(self, index):
        if 0 <= index < len(self.__list_of_games):
            return self.__list_of_games[index]
        else:
            return None

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.__current >= len(self.__list_of_games):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_games[self.__current - 1]
