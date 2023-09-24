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

        return self.__publisher_name

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

        return self.__genre_name

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
        self.__categories = set()
        self.__tags = set()
        self.__reviews = list()
        self.__price = None
        self.__release_date = None
        self.__description = None
        self.__publisher = None
        self.__image_url = None
        self.__website_url = None
        self.__video_url = None
        self.__languages = list()
        self.__system_dict = dict()

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
    def genres(self) -> list[Genre]:
        """
        Return the list of genres of a game object

        :return: list
        """

        return self.__genres

    @property
    def categories(self) -> set:
        """
        Return the list of categories of a game object

        :return: list
        """

        return self.__categories

    @property
    def tags(self) -> set:
        """
        Return the list of tags of a game object

        :return: set
        """

        return self.__tags

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

    def remove_genre(self, genre_to_remove: Genre) -> None:
        """
        Removes a Genre object from the game's list of genres.
        Does nothing if Genre is invalid or doesn't exist.

        Parameters
        ----------
        genre_to_remove: Genre
            This is a Genre object to be removed.
        :param genre_to_remove: Genre
        :return: None
        """

        if isinstance(genre_to_remove, Genre) and genre_to_remove \
                in self.__genres:
            self.__genres.remove(genre_to_remove)
        else:
            print(f'Could not find {genre_to_remove} in list of genres.')

    """Added the following methods in Games class for games-description page"""

    def add_review(self, review):
        if isinstance(review, Review) and review not in self.__reviews:
            self.__reviews.append(review)

    def add_language(self, language):
        if len(language.strip()) > 0:
            self.__languages.append(language)

    @property
    def system_dict(self):
        return self.__system_dict

    @property
    def languages(self):
        return self.__languages

    @property
    def video_url(self):
        return self.__video_url

    @video_url.setter
    def video_url(self, new_video_url: str) -> None:

        if isinstance(new_video_url, str) and new_video_url.strip():
            self.__video_url = new_video_url.strip()
        else:
            self.__video_url = None

    def add_category(self, new_category: str) -> None:
        """
        Adds a new category to the game's list of categories.
        Does nothing if category is invalid or duplicate.

        Parameters
        ----------
        new_category: str
            This is a category to be added.
        :param new_category: str
        :return: None
        """

        if isinstance(new_category, str) and new_category.strip() \
                and new_category not in self.__categories:
            self.__categories.add(new_category.strip())

    def remove_category(self, category_to_remove: str) -> None:
        """
        Removes a category from the game's list of categories.
        Does nothing if category is invalid or doesn't exist.

        Parameters
        ----------
        category_to_remove: str
            This is a category to be removed.
        :param category_to_remove: str
        :return: None
        """

        if isinstance(category_to_remove, str) \
                and category_to_remove.strip() \
                and category_to_remove in self.__categories:
            self.__categories.remove(category_to_remove.strip())
        else:
            print(f'Could not find {category_to_remove} '
                  f'in list of categories.')

    def add_tag(self, new_tag: str) -> None:
        """
        Adds a new tag to the game's list of tags.
        Does nothing if tag is invalid or duplicate.

        Parameters
        ----------
        new_tag: str
            This is a tag to be added.
        :param new_tag: str
        :return: None
        """

        if isinstance(new_tag, str) and new_tag.strip() \
                and new_tag not in self.__tags:
            self.__tags.add(new_tag.strip())

    def remove_tag(self, tag_to_remove: str) -> None:
        """
        Removes a tag from the game's list of tags.
        Does nothing if tag is invalid or doesn't exist.

        Parameters
        ----------
        tag_to_remove: str
            This is a tag to be removed.
        :param tag_to_remove: str
        :return: None
        """

        if isinstance(tag_to_remove, str) \
                and tag_to_remove.strip() \
                and tag_to_remove in self.__tags:
            self.__tags.remove(tag_to_remove.strip())
        else:
            print(f'Could not find {tag_to_remove} in list of tags.')


class User:
    def __init__(self, username: str, password: str) -> None:
        """
        Initialise a User object.

        Parameters
        ----------
        username: str
            A non-empty string for the username, stored in lowercase.
        password: str
            A string for the password, must be at least 7 characters.
        :param username: str

        :param password: str
        :return None
        :raise ValueError
        """

        if isinstance(username, str) and username.strip():
            self.__username = username.lower().strip()
        else:
            raise ValueError("Username must be a non-empty string.")
        if isinstance(password, str) and len(password.strip()) > 6:
            self.__password = password
        else:
            raise ValueError("Password must be string with min length of 7.")

        self.__favourite_games: list[Game] = list()
        self.__reviews: list[Review] = list()
        self.__wishlist = Wishlist(self)

    def __repr__(self) -> str:
        """
        Return the string representation of a User object.

        :return: str
        """

        return f'<User {self.__username}>'

    def __eq__(self, other) -> bool:
        """
        Returns True if one User is equal to the other.

        Parameters
        ----------
        other: User
            This is the other User object ot compare with.
        :param other: User
        :return: bool
        """

        if isinstance(other, self.__class__):
            return self.__username == other.__username
        else:
            return False

    def __lt__(self, other) -> bool:
        """
        Returns True if this User object is less than the other User.
        Comparison is based on the username.

        Parameters
        ----------
        other: User
        This is the other User object to compare with.
        :param other: User
        :return: bool
        """

        if isinstance(other, self.__class__):
            return self.__username < other.__username

    def __hash__(self) -> int:
        """
        Returns the hash value of a User object.
        Hash value based on username.
        :return: int
        """

        return hash(self.__username)

    @property
    def username(self) -> str:
        """
        Return the username.
        :return: str
        """

        return self.__username

    @property
    def password(self) -> str:
        """
        Return the user's password.
        :return: str
        """

        return self.__password

    @property
    def favourite_games(self) -> list[Game]:
        """
        Return a list of the User's favourite games.

        :return: list
        """

        return self.__favourite_games

    @property
    def reviews(self) -> list:
        """
        Return a list of the User's reviews.

        :return: list
        """

        return self.__reviews

    def add_favourite_game(self, game_to_add: Game) -> None:
        """
        Adds a Game object to the User's list of favourite games.

        Parameters
        ----------
        game_to_add: Game
            This is the game to add.

        :param game_to_add: Game
        :return: None
        """

        if (isinstance(game_to_add, Game) and game_to_add
                not in self.__favourite_games):
            self.__favourite_games.append(game_to_add)
        else:
            return None

    def remove_favourite_game(self, game_to_remove: Game) -> None:
        """
        Removes a Game object from the User's list of favourite games.

        Parameters
        ----------
        game_to_remove: Game
            This is the Game object to delete
        :param game_to_remove: Game
        :return: None
        """

        if isinstance(game_to_remove, Game) and game_to_remove \
                in self.__favourite_games:
            self.__favourite_games.remove(game_to_remove)
        else:
            return None

    def add_review(self, review_to_add) -> None:
        """
        Add a review to the user's list of reviews.

        Parameters
        ----------
        review_to_add: Review
            This is the Review object to add.

        :param review_to_add:
        :return: None
        """

        if isinstance(review_to_add, Review) and review_to_add \
                not in self.__reviews:
            self.__reviews.append(review_to_add)
        else:
            return None

    def remove_review(self, review_to_remove) -> None:
        """
        Remove a review from the user's list of reviews.

        Parameters
        ----------
        review_to_remove: Review
            This is the Review object to remove

        :param review_to_remove: Review
        :return: None
        """

        if isinstance(review_to_remove, Review) and review_to_remove \
                in self.__reviews:
            self.__reviews.remove(review_to_remove)
        else:
            return None

    def get_wishlist(self):
        return self.__wishlist


class Review:
    def __init__(self, user: User, game: Game,
                 rating: int, comment: str, timestamp=None) -> None:
        """
        Initialise a Review Object.
        Raise ValueError if parameters invalid.

        Parameters
        ----------
        user: Game
            The user that the review is associated with.
        game: Game
            This is the game the review is associated with.
        rating: int
            The rating of the review (0 to 5 inclusive).
        comment: str
            The review text.

        :param user: User
        :param game: Game
        :param rating: int
        :param comment: str
        :return None
        :raise ValueError
        """
        if isinstance(user, User):
            self.__user = user
        else:
            raise ValueError('User must be instance of User class.')

        if isinstance(game, Game):
            self.__game = game
        else:
            raise ValueError('Game must be instance of Game class.')

        if isinstance(rating, int) and (0 <= rating <= 5):
            self.__rating = rating
        else:
            raise ValueError('Rating must be integer from 0 to 5 inclusive.')

        if isinstance(comment, str) and comment.strip():
            self.__comment = comment.strip()
        else:
            raise ValueError('Comment must be non-empty string.')

        if timestamp is None:
            self.__timestamp = datetime.utcnow().strftime("%d %B %Y %I:%M:%S")
        else:
            self.__timestamp = timestamp

    def __repr__(self) -> str:
        """
        Returns the string representation of the Review object.
        :return: str
        """

        return (f'Review(User: {self.__user}, Game: {self.__game}, ' +
                f'Rating: {self.__rating}, Comment: {self.__comment})')

    def __eq__(self, other) -> bool:
        """
        Returns True if the other Review object matches this object.
        Comparison based on user, game, rating and comment.

        Parameters
        ----------
        other: Review
            The other Review object to compare with
        :param other: Review
        :return: bool
        """

        if not isinstance(other, Review):
            return False

        return self.__user == other.user \
            and self.__game == other.game \
            and self.__comment == other.comment

    @property
    def user(self) -> User:
        """
        Return the user associated with the review.
        :return: User
        """

        return self.__user

    @property
    def game(self) -> Game:
        """
        Return the game associated with the review.
        :return: Game
        """

        return self.__game

    @property
    def comment(self) -> str:
        """
        Return the comment associated with the review.
        :return: str
        """

        return self.__comment

    @property
    def rating(self) -> int:
        """
        Return the rating associated with the review.
        :return: int
        """

        return self.__rating

    @comment.setter
    def comment(self, new_comment: str) -> None:
        """
        Sets the new comment associated with the review.
        Comment must be a non-empty string.

        Parameters
        ----------
        new_comment: str
            This is the new comment to be set.
        :param new_comment: str
        :return: None
        :raise ValueError
        """

        if isinstance(new_comment, str) and new_comment.strip():
            self.__comment = new_comment.strip()
        else:
            raise ValueError("Comment must be non-empty string.")

    @property
    def timestamp(self):
        return self.__timestamp

    @rating.setter
    def rating(self, new_rating: int) -> None:
        """
        Sets the new rating associated with the review.
        Rating must be an integer between 0 and 5 inclusive.

        Parameters
        ----------
        new_rating: int
            This is the new rating to be set
        :param new_rating: int
        :return: None
        :raise ValueError
        """

        if isinstance(new_rating, int) and (0 <= new_rating <= 5):
            self.__rating = new_rating
        else:
            raise ValueError('Rating must be integer from 0 to 5 inclusive')


class Wishlist:
    def __init__(self, user: User) -> None:
        """
        Initialises the Wishlist object.

        :return: None
        """

        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user

        self.__list_of_games = []

    def __iter__(self):
        """
        Initialise the iterator and return the Wishlist object.

        :return: Wishlist
        """

        self.__iterator_index = 0
        return self

    def __next__(self) -> Game:
        """
        Return the next Game object from the wishlist.

        :return: Game
        :raise: StopIteration
            When there are no more games to return.
        """

        if self.__iterator_index < len(self.__list_of_games):
            game = self.__list_of_games[self.__iterator_index]
            self.__iterator_index += 1
            return game
        else:
            raise StopIteration

    def add_wish_game(self, game_to_add: Game) -> None:
        """
        Append a Game object to the wishlist.

        Parameters
        ----------
        game_to_add: Game
            The game object that will be appended to the wishlist
        :param game_to_add:
        :return: None
        """

        if (isinstance(game_to_add, Game) and game_to_add
                not in self.__list_of_games):
            self.__list_of_games.append(game_to_add)

    def remove_game(self, game_to_remove: Game) -> None:
        """
        Remove a Game object from the wishlist if present.

        Parameters
        ----------
        game_to_remove: Game
            The game object that will be appended to the wishlist
        :param game_to_remove:
        :return: None
        """

        if (isinstance(game_to_remove, Game) and game_to_remove
                in self.__list_of_games):
            self.__list_of_games.remove(game_to_remove)

    def select_game(self, index: int) -> Game:
        """
        Return a game object from the wishlist from the specified index.

        Parameters
        ----------
        index: int
            The index of the wishlist to access.
        :param index: int
        :return: Game
        """

        if isinstance(index, int) and (0 <= index < len(self.__list_of_games)):
            return self.__list_of_games[index]

    def size(self) -> int:
        """
        Return the number of games in the wishlist.
        :return: int
        """

        wishlist_size = len(self.__list_of_games)
        if wishlist_size > 0:
            return wishlist_size

    def first_game_in_list(self) -> Game | None:
        """
        Return the first game in the Wishlist.
        :return: Game | None
        """

        if self.__list_of_games:
            return self.__list_of_games[0]
        else:
            return None

    def list_of_games(self) -> list[Game]:
        """
        Return the list of game objects.
        :return: list[Game]
        """
        return self.__list_of_games

