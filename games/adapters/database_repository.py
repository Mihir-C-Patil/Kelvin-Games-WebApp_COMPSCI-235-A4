from typing import List, Any

from sqlalchemy import func, orm
from sqlalchemy.orm import scoped_session, contains_eager
from sqlalchemy.orm.exc import NoResultFound

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import *


class SessionContextManager:
    """
    SessionContextManager

    Class representing a context manager for managing SQLAlchemy
    sessions.

    Parameters:
    - session_factory: SQLAlchemy session factory

    Attributes:
    - session: Current SQLAlchemy session

    Methods:
    - __enter__(): Enter the context manager
    - __exit__(*args): Exit the context manager and rollback the session
    - commit(): Commit the session
    - rollback(): Rollback the session
    - reset_session(): Reset the session by closing the current session
    and creating a new one
    - close_current_session(): Close the current session
    """

    def __init__(self, session_factory):
        """
        Initializes a new instance of SessionContextManager.

        Args:
            session_factory: A session factory object used to create new
            database sessions.
        """
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        """
        Context manager method for entering the session context.

        Parameters:
            None

        Returns:
            SessionContextManager: The current instance of the
            SessionContextManager.

        Example usage:
            with SessionContextManager() as session_manager:
                # perform database operations
        """
        return self

    def __exit__(self, *args):
        """
        Closes the session and rolls back any pending transactions.

        Args:
            *args: Additional arguments, if any.

        """
        self.rollback()

    @property
    def session(self):
        """
        Get the current session.

        Returns:
        The current session.

        """
        return self.__session

    def commit(self):
        """
        Commits the current transaction.

        This method commits the current transaction using the SQLAlchemy
        session object associated with the `SessionContextManager`
        instance.

        Parameters:
        None

        Returns:
        None

        Example Usage:
        manager = SessionContextManager()
        manager.commit()
        """
        self.__session.commit()

    def rollback(self):
        """
        Rollbacks the current transaction.

        Parameters:
        None

        Return type:
        None

        """
        self.__session.rollback()

    def reset_session(self):
        """
        Resets the current session of the SessionContextManager.

        This method closes the current session using the
        `close_current_session` method and creates a new scoped session
        using the `scoped_session` method with the session factory
        stored in the `__session_factory` attribute.

        Parameters:
        None

        Returns:
        None

        Example Usage:
        session_context_manager = SessionContextManager()
        session_context_manager.reset_session()
        """
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        """
        Closes the current session.

        This method closes the current session if it is not None.

        Returns:
            None

        Example:
            >>> session_manager = SessionContextManager()
            >>> session_manager.close_current_session()
        """
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    """
    Class representing the repository for interacting with the database
    using SQLAlchemy.

    Attributes: - _session_cm: SessionContextManager: The session context
    manager used to manage session context.

    Methods:
        - __init__(session_factory: Any): Initializes the class by
          setting the session context manager.
        - close_session(): Closes the current session.
        - reset_session(): Resets the session.
        - add_user(user: User): Adds a user to the repository.
        - get_user(username: str) -> Any | None: Gets a user from the
          repository by its username.
        - add_genre(genre: Genre) -> None: Adds a genre to the
          repository.
        - get_genres() -> List[Genre]: Gets all genres from the
          repository.
        - add_publisher(publisher): Adds a publisher to the repository.
        - get_publishers() -> List[Publisher]: Gets all publishers from
          the repository.
        - get_genre_of_games(target_genre: Genre) -> List[Game]: Gets
          all games with a particular genre from the repository.
        - add_game(game: Game): Adds a game to the repository.
        - get_games() -> List[Game]: Gets all games from the repository.
        - get_slide_games() -> List[Game]: Gets all slide games from the
          repository.
        - get_number_of_games(): Gets the number of games from the
          repository.
        - get_games_by_id(game_id: int): Gets a game from the repository
          by its ID.
        - get_similar_games(genres_list: List[Genre]): Gets all games
          with similar genres from the repository.
        - search_games_by_title(game_title: str) -> List[Game]: Searches
          games by their titles in the repository.
        - search_games_by_publisher(query: str) -> List[Game]: Searches
          games by their publishers in the repository.
        - search_games_by_category(query: str) -> List[Game]: Searches
          games by their categories in the repository.
        - search_games_by_tags(query: str) -> List[Game]: Searches games
          by their tags in the repository.
        - add_wish_game(user, game): Adds a game to the wishlist of a
          user in the repository.
        - remove_wish_game(user, game): Removes a game from the wishlist
          of a user in the repository.
        - get_wishlist(user): Gets the wishlist of a user from the
          repository.
        - add_review(user, game, rating, review_text): Adds or updates a
          review for a game by a user in the repository.
        - get_user_review(user): Gets all reviews written by a user from
          the repository.
    """

    def __init__(self, session_factory):
        """
        Args:
            session_factory: The session factory used to create sessions
            for accessing the database.

        """
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        """
        Closes the current session.

        This method is used to close the current session in the
        SqlAlchemyRepository object.

        Parameters:
            None

        Returns:
            None

        """
        self._session_cm.close_current_session()

    def reset_session(self):
        """
        Resets the current session by calling the reset_session method
        of the session context manager.

        Parameters:
        - None

        Returns:
        - None
        """
        self._session_cm.reset_session()

    def add_user(self, user: User):
        """
        Add a user to the repository.

        Args:
            user (User): The user object to add.

        """
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> Any | None:
        """
        Args:
            username: A string representing the username of the user.

        Returns:
            An instance of the User class representing the user if
            found, or None if the user is not found.

        """
        try:
            user = self._session_cm.session.query(User).filter(
                func.lower(User._User__username) \
                == func.lower(username)).one()
            return user
        except NoResultFound:
            return None

    def add_genre(self, genre: Genre) -> None:
        """
        Args:
            genre: The Genre object to be added to the repository.
        """
        with self._session_cm as scm:
            existing_genre = scm.session.query(Genre) \
                .filter_by(genre_name=genre.genre_name).first()
            if existing_genre is None:
                scm.session.merge(genre)
                scm.commit()

    def get_genres(self) -> List[Genre]:
        """
        Returns a list of all genres in the repository.

        :return: A list of Genre objects.
        :rtype: List[Genre]
        :raises: None
        """
        genres = None
        try:
            genres = self._session_cm.session.query(Genre).all()
        except NoResultFound:
            pass
        return genres

    def add_publisher(self, publisher):
        """
        Args:
            publisher: The object representing the publisher to be added
            to the repository.

        """
        with self._session_cm as scm:
            existing_publisher = scm.session.query(Publisher).filter_by(
                publisher_name=publisher.publisher_name).first()
            if existing_publisher is None:
                scm.session.merge(publisher)
                scm.commit()
            pass

    def get_publishers(self) -> list[Publisher]:
        """

        Retrieve a list of all publishers from the repository.

        :return: A list of Publisher objects.
        :rtype: list[Publisher]
        """
        publishers = None
        try:
            publishers = self._session_cm.session.query(Publisher).all()
        except NoResultFound:
            pass
        return publishers

    def get_genre_of_games(self, target_genre) -> List[Game]:
        """
        Args:
            target_genre (str): The genre of games to retrieve.

        Returns:
            List[Game]: A list of games with the specified genre.

        """
        games = None
        try:
            games = (
                self._session_cm.session.query(Game)
                .join(Game._Game__genres)
                .filter(Genre._Genre__genre_name == target_genre)
                .options(contains_eager(Game._Game__genres))
                .all()
            )
        except NoResultFound:
            pass
        return games

    def add_game(self, game: Game):
        """
        Args:
            game (Game): The game object to be added to the repository.

        """
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def get_games(self) -> List[Game]:
        """
        Retrieves a list of all games stored in the repository.

        :return: A list of Game objects representing the games.
        """
        games = None
        try:
            games = self._session_cm.session.query(Game).all()
        except NoResultFound:
            pass
        return games

    def get_slide_games(self) -> List[Game]:
        """

            Returns a list of slide games.

            Retrieves all slide games from the repository.

            Returns:
                List[Game]: A list of Game objects representing slide
                games.

        """
        games = None
        try:
            games = self._session_cm.session.query(Game).all()
        except NoResultFound:
            pass
        return games

    def get_number_of_games(self):
        """
        Returns the number of games in the repository.

        Returns:
            int: The number of games in the repository.
        """
        number_of_games = self._session_cm.session.query(Game).count()
        return number_of_games

    def get_games_by_id(self, game_id: int):
        """
        Args:
            game_id (int): The ID of the game to retrieve.

        Returns:
            Game: The game with the specified ID, or None if no game is
            found.
        """
        game = None
        try:
            game = (self._session_cm.session.query(Game)
                    .filter(Game._Game__game_id == game_id).one())
        except NoResultFound:
            pass
        return game

    def get_similar_games(self, genres_list):
        """
        Retrieves a list of similar games based on the provided genres.

        Args:
            genres_list (List[str]): A list of genres to search for.

        Returns:
            List[Game]: A list of Game objects that match the provided
            genres. If no matches are found, an empty list is returned.
        """
        games = None
        try:
            games = (
                self._session_cm.session.query(Game)
                .join(Game._Game__genres)
                .filter(Genre == genres_list[0])
                .options(contains_eager(Game._Game__genres))
                .all()
            )
        except NoResultFound:
            pass
        return games

    def search_games_by_title(self, game_title: str) -> List[Game]:
        """
        Searches for games by title.

        Args:
            game_title: The title of the game to search for.

        Returns:
            A list of Game objects that match the given title.
        """
        game_title = game_title.lower()
        games = None
        try:
            games = (self._session_cm.session.query(Game)
                     .filter(
                func.lower(Game._Game__game_title).contains(game_title)).all())
        except NoResultFound:
            pass
        return games

    def search_games_by_publisher(self, query: str) -> List[Game]:
        """Searches for games by publisher name.

        Args:
            query(str): The query string to search for games by
            publisher.

        Returns:
            List[Game]: A list of Game objects matching the query.

        """
        query = query.lower()
        games = None
        try:
            games = (self._session_cm.session.query(Game)
                     .join(Publisher)
                     .filter(
                func.lower(Publisher._Publisher__publisher_name).contains(
                    query)).all())
        except NoResultFound:
            pass
        return games

    def search_games_by_category(self, query: str) -> List[Game]:
        """
        Searches for games by category in the SqlAlchemy database.

        Args:
            query (str): The category to search for.

        Returns:
            List[Game]: A list of games that match the specified
            category.
        """
        query = query.lower()
        games = None
        try:
            games = (self._session_cm.session.query(Game)
                     .join(Game._Game__genres)
                     .join(Genre)
                     .filter(
                func.lower(Genre._Genre__genre_name).contains(query)).all())
        except NoResultFound:
            pass
        return games

    def search_games_by_tags(self, query: str) -> List[Game]:
        """
        Searches for games in the repository based on tags.

        Args:
            query (str): The query string for searching games by tags.

        Returns:
            List[Game]: A list of Game objects matching the given query.
            If no games are found, an empty list is returned.
        """
        query = query.lower()
        games = None
        try:
            games = (self._session_cm.session.query(Game)
                     .filter(
                func.lower(Game._Game__tags_string).contains(query)).all())
        except NoResultFound:
            pass
        return games

    def add_wish_game(self, user, game):
        """
        Adds a game to the wishlist of a user.

        Args:
            user: User object representing the user.
            game: Game object representing the game to be added.

        """
        with self._session_cm as scm:
            try:
                user_ = scm.session.query(User).filter(
                    func.lower(User._User__username) == func.lower(
                        user.username)).first()
                game_ = scm.session.query(Game).filter(
                    Game._Game__game_id == game.game_id).first()
                if user_ and game_:
                    user._User__wishlist._Wishlist__games.append(game)
                    scm.session.commit()
                    print(
                        f"Game '{game._Game__game_title}' added to wishlist "
                        f"for user '{user._User__username}'.")
                else:
                    print("User or game not found.")
            except Exception as e:
                print(f"Error adding game to wishlist: {str(e)}")
            finally:
                scm.session.close()

    def remove_wish_game(self, user, game):
        """
        Removes a game from the wishlist of a user.

        Args:
            user: The user for whom the game should be removed from the
            wishlist.
            game: The game to be removed from the wishlist.

        """
        with self._session_cm as scm:
            try:
                user_ = scm.session.query(User).filter(
                    func.lower(User._User__username) == func.lower(
                        user.username)).first()
                game_ = scm.session.query(Game).filter(
                    Game._Game__game_id == game.game_id).first()
                if user_ and game_:
                    user_._User__wishlist._Wishlist__games.remove(game)
                    scm.session.commit()
                    print(
                        f"Game '{game._Game__game_title}' removed from "
                        f"wishlist for user '{user_._User__username}'.")
                else:
                    print("User or game not found.")
            except Exception as e:
                print(f"Error removing game from wishlist: {str(e)}")
            finally:
                scm.session.close()

    def get_wishlist(self, user):
        """
        Retrieves the wishlist games for a given user.

        Args:
            user: A User object representing the user for whom wishlist
            games are to be retrieved.

        Returns:
            wishlist_games: A list of Game objects representing the
            games in the user's wishlist, or None if the user is not
            found or an error occurs.
        """
        with self._session_cm as scm:
            try:
                user_ = scm.session.query(User).filter(
                    func.lower(User._User__username) == func.lower(
                        user.username)).first()

                if user_:
                    wishlist_games = user_._User__wishlist._Wishlist__games
                    return wishlist_games
                else:
                    print("User not found.")
                    return None
            except Exception as e:
                print(f"Error getting user wishlist: {str(e)}")
                return None
            finally:
                scm.session.close()

    def add_review(self, user, game, rating, review_text):
        """
        Args:
            user: User object representing the user who wrote the review.
            game: Game object representing the game being reviewed.
            rating: An integer representing the rating given by the user.
            review_text: A string representing the text of the review.

        Returns:
            True if the review was successfully added or updated.
            False if the user has already reviewed the game or if there
            was an error.
        """
        with self._session_cm as scm:
            try:
                user_ = scm.session.query(User).filter(
                    func.lower(User._User__username) == func.lower(
                        user.username)).first()
                game_ = scm.session.query(Game).filter(
                    Game._Game__game_id == game.game_id).first()

                if user_ and game_:
                    existing_review = scm.session.query(Review).filter(
                        Review._Review__user == user_,
                        Review._Review__game == game_
                    ).first()

                    if existing_review:
                        return False
                    else:
                        new_review = Review(
                            user_,
                            game_,
                            rating,
                            review_text,
                        )
                        scm.session.add(new_review)
                        scm.session.commit()
                        print(
                            f"Review added for game '{game_._Game__game_title}\
                            ' by user '{user_._User__username}'.")
                    return True
                else:
                    print("User or game not found.")
            except Exception as e:
                print(f"Error adding or updating review: {str(e)}")
                scm.session.rollback()
            finally:
                scm.session.close()

    def get_user_review(self, user):
        """
        Args:
            user: A User object representing the user for which we want
            to retrieve the reviews.

        Returns:
            A list of Review objects representing the reviews provided
            by the given user,
            or None if the user is not found.
        """
        with self._session_cm as scm:

            user = scm.session.query(User).filter(
                func.lower(User._User__username) == func.lower(
                    user.username)).first()

            if user:
                user_with_reviews = scm.session.query(User).options(
                    orm.joinedload('reviews')).get(user.id)
                return user_with_reviews.reviews
            else:
                return None
