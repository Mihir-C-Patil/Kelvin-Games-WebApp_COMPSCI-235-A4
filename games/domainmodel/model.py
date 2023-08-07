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

    def __repr__(self) -> str:
        """
        Return a string representation of a Game object

        :return: str
        """

        return f'<Game {self.__game_id}, {self.__game_title}>'

    def __eq__(self, other) -> bool:
        """
        Return a boolean value which is True if two game IDs are equal.
        Comparison is based on the Game ID.

        Parameters
        ----------
        other: Game
            The other Game object to compare with

        :param other: Game
        :return: bool
        """

        if not isinstance(other, self.__class__):
            return False
        else:
            return self.__game_id == other.game_id

    def __lt__(self, other) -> bool:
        """
        Return True if the Game object is less than the other game
        object. Comparison is based on the Game ID.

        Parameters
        ----------
        other: Game
            The other Game object to compare with

        :param other: Game
        :return: bool
        """

        if not isinstance(other, self.__class__):
            return False
        return self.__game_id < other.game_id

    def __hash__(self) -> int:
        """
        Returns the hash value of a Game object based on the game ID.

        :return: int
        """

        return hash(self.__game_id)

    @property
    def game_id(self) -> int:
        """
        Return the id number of the game.

        :return: int
        """

        return self.__game_id

    @property
    def title(self) -> str:
        """
        Return the title of the game.

        :return: str
        """

        return self.__game_title

    @property
    def genres(self) -> list:
        """
        Return the list of genres of a game object

        :return: list
        """

        return self.__genres

    @property
    def reviews(self) -> list:
        """
        Return the list of reviews of a game object

        :return: list
        """

        return self.__reviews

    @property
    def price(self) -> (int, float):
        """
        Return the price of the game

        :return: (int, float)
        """

        return self.__price

    @property
    def release_date(self) -> datetime:
        """
        Return the release date of the game.

        :return: datetime
        """

        return self.__release_date

    @property
    def description(self) -> str:
        """
        Return the description of the game.

        :return: str
        """

        return self.__description

    @property
    def publisher(self) -> Publisher:
        """
        Return the publisher of the game, as a Publisher object

        :return: Publisher
        """

        return self.__publisher

    @property
    def image_url(self) -> str:
        """
        Return the image URL of the game.

        :return: str
        """

        return self.__image_url

    @property
    def website_url(self) -> str:
        """
        Return the website URL of the game.

        :return: str
        """

        return self.__website_url

    @title.setter
    def title(self, new_title: str) -> None:
        """
        Sets the new title of the game. Sets to None if invalid.

        Parameters
        ----------
        new_title: str
            This is the new title of the game.

        :param new_title: str
        :return: None
        """

        if isinstance(new_title, str) and new_title.strip():
            self.__game_title = new_title.strip()
        else:
            self.__game_title = None

    @price.setter
    def price(self, new_price: (int, float)) -> None:
        """
        Sets the new price of the game. Raises ValueError if invalid.

        Parameters
        ----------
        new_price: (int, float)
            The new price of the game (must be non-negative number)

        :param new_price:
        :return: None
        :raise ValueError
        """

        if isinstance(new_price, (int, float)) and new_price >= 0:
            self.__price = new_price
        else:
            raise ValueError("Price must be a non-negative value.")

    @release_date.setter
    def release_date(self, new_date: str) -> None:
        """
        Set the release date of the game. Raises ValueError if invalid.

        Parameters
        ----------
        new_date: str
            The new release date of the game, must be in '%b %d, %Y'
            format.
        :param new_date: str
        :return: None
        :raise ValueError
        """

        if isinstance(new_date, str) and new_date.strip():
            try:
                datetime.strptime(new_date, "%b %d, %Y")
                self.__release_date = new_date
            except ValueError:
                raise ValueError("Invalid release date format. "
                                 "Use '%b %d, %Y'")
        else:
            raise ValueError("Date must be in format: %b %d, %Y")

    @description.setter
    def description(self, new_description: str) -> None:
        """
        Sets the new description of the game. Sets to None if invalid

        Parameters
        ----------
        new_description: str
            The new description of the game, must be a non-empty string.
        :param new_description: str
        :return: None
        """

        if isinstance(new_description, str) and new_description.strip():
            self.__description = new_description.strip()
        else:
            self.__description = None

    @publisher.setter
    def publisher(self, new_publisher: Publisher) -> None:
        """
        Sets the new publisher of a game.

        Parameters
        ----------
        new_publisher: Publisher
            This is a Publisher object
        :param new_publisher:
        :return: None
        """

        if isinstance(new_publisher, Publisher):
            self.__publisher = new_publisher
        else:
            self.__publisher = None

    @image_url.setter
    def image_url(self, new_image_url: str) -> None:
        """
        Sets the image URL of the game's cover image.

        Parameters
        ----------
        new_image_url: str
            The full URL of the game's cover image
        :param new_image_url: str
        :return: None
        """

        if isinstance(new_image_url, str) and new_image_url.strip():
            self.__image_url = new_image_url.strip()
        else:
            self.__image_url = None

    @website_url.setter
    def website_url(self, new_website_url: str) -> None:
        """
        Sets the URL of the game's website.

        Parameters
        ----------
        new_website_url: str
            This is the full URL of the game's website
        :param new_website_url:
        :return: None
        """

        if isinstance(new_website_url, str) and new_website_url.strip():
            self.__website_url = new_website_url.strip()
        else:
            self.__website_url = None

    def add_genre(self, new_genre: Genre) -> None:
        """
        Adds a new Genre object to the game's list of genres.
        Does nothing if genre is invalid or duplicate.

        Parameters
        ----------
        new_genre: Genre
            This is a Genre object to be added.
        :param new_genre: Genre
        :return: None
        """

        if isinstance(new_genre, Genre) and new_genre not in self.__genres:
            self.__genres.append(new_genre)
        return None

    def remove_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return
        try:
            self.__genres.remove(genre)
        except ValueError:
            print(f"Could not find {genre} in list of genres.")
            pass


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
