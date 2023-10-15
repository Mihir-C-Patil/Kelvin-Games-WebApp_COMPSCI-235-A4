from abc import ABC
from bisect import insort_left
from typing import List

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import *


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

    def add_wish_game(self, user, game):
        """
        Args:
            user: User object representing the user who wants to add a
            game to their wishlist.
            game: Game object representing the game that the user wants
            to add to their wishlist.

        """
        user.get_wishlist().add_wish_game(game)

    def remove_wish_game(self, user, game):
        """
        Removes a game from the wishlist of a user.

        Args:
            user: The user for whom the game should be removed from
            their wishlist.
            game: The game to be removed from the user's wishlist.
        """
        user.get_wishlist().remove_game(game)

    def get_wishlist(self, user):
        """
        Args:
            user: User object representing the user whose wishlist is to
            be retrieved.

        Returns:
            List of Game objects representing the games in the user's
            wishlist.
        """
        return user.get_wishlist().list_of_games()

    def add_review(self, user, game, rating, review):
        """
        Args:
            user: User object representing the author of the review.
            game: Game object representing the game being reviewed.
            rating: Numeric value representing the rating given in the
            review.
            review: String representing the content of the review.

        """
        new_review = Review(user, game, rating, review)
        if len(game.reviews) == 0:
            user.add_review(new_review)
            game.add_review(new_review)
            return True
        else:
            for review in game.reviews:
                if user == review.user:
                    return False
        user.add_review(new_review)
        game.add_review(new_review)
        return True

    def get_user_review(self, user):
        """
        Retrieves the reviews submitted by a specific user.

        Args:
            user: The user whose reviews should be retrieved.

        Returns:
            A list of reviews submitted by the specified user.
        """
        return user.reviews
