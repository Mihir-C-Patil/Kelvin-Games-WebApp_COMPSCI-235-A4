import os.path
from abc import ABC
from bisect import insort_left
from typing import List
from pathlib import Path
from games.domainmodel.model import *
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.repository import AbstractRepository

from sqlalchemy import desc, asc, or_, func, orm
from sqlalchemy.orm import scoped_session, contains_eager
from sqlalchemy.orm.exc import NoResultFound


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User) -> None:
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(
                User._User__username == username).one()
        except NoResultFound:
            pass
        return user

    def add_genre(self, genre: Genre) -> None:
        with self._session_cm as scm:
            existing_genre = scm.session.query(Genre).filter_by(genre_name=genre.genre_name).first()
            if existing_genre is None:
                scm.session.merge(genre)
                scm.commit()
            pass

    def get_genres(self) -> List[Genre]:
        genres = None
        try:
            genres = self._session_cm.session.query(Genre).all()
        except NoResultFound:
            pass
        return genres

    def add_publisher(self, publisher) -> None:
        with self._session_cm as scm:
            existing_publisher = scm.session.query(Publisher).filter_by(publisher_name=publisher.publisher_name).first()
            if existing_publisher is None:
                scm.session.merge(publisher)
                scm.commit()
            pass

    def get_publishers(self) -> list[Publisher]:
        publishers = None
        try:
            publishers = self._session_cm.session.query(Publisher)
        except NoResultFound:
            pass
        return publishers

    def get_game_tags(self) -> list[str]:
        tags = None
        try:
            tags = list(self._session_cm.session.query(Game._Game__tags_string).all())
        except NoResultFound:
            pass
        return tags

    def get_genre_of_games(self, target_genre) -> List[Game]:
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
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def get_games(self) -> List[Game]:
        games = None
        try:
            games = self._session_cm.session.query(Game).all()
        except NoResultFound:
            pass
        return games

    def get_slide_games(self) -> List[Game]:
        games = None
        try:
            games = self._session_cm.session.query(Game).all()
        except NoResultFound:
            pass
        return games

    def get_number_of_games(self):
        number_of_games = self._session_cm.session.query(Game).count()
        return number_of_games

    def get_games_by_id(self, game_id: int):
        game = None
        try:
            game = (self._session_cm.session.query(Game)
                    .filter(Game._Game__game_id == game_id).one())
        except NoResultFound:
            pass
        return game

    def get_similar_games(self, genre):
        games = None
        try:
            # games = (self._session_cm.session.query(Game)
            #          .filter(Game._Game__genres.contains(genre)).all())
            games = (
                self._session_cm.session.query(Game)
                .filter(
                    or_(*(Game._Game__genres.contains(g) for g in genre))
                )
                .all()
            )
        except NoResultFound:
            pass
        return games

    def search_games_by_title(self, game_title: str) -> (List[Game], None):
        game_title = game_title.lower()
        games = None
        try:
            (self._session_cm.session.query(Game)
             .filter(game_title in Game._Game__game_title).all())
        except NoResultFound:
            pass
        return games

    def search_games_by_publisher(self, query) -> (List[Game], None):
        query = query.lower()
        games = None
        try:
            games = (self._session_cm.session.query(Game)
                     .filter(query in Game._Game__publisher).all())
        except NoResultFound:
            pass
        return games

    def search_games_by_category(self, query) -> (List[Game], None):
        query = query.lower()
        games = None
        try:
            games = (self._session_cm.session.query(Game)
                     .filter(query in Game._Game__categories).all())
        except NoResultFound:
            pass
        return games

    def search_games_by_tags(self, query) -> (List[Game], None):
        query = query.lower()
        games = None
        try:
            games = (self._session_cm.session.query(Game)
                     .filter(query in Game._Game__tags_string).all())
        except NoResultFound:
            pass
        return games

    def add_wish_game(self, user, game):
        with self._session_cm as scm:
            try:
                user_ = scm.session.query(User).filter(func.lower(User._User__username) == func.lower(user.username)).first()
                game_ = scm.session.query(Game).filter(Game._Game__game_id == game.game_id).first()
                if user_ and game_:
                    user._User__wishlist._Wishlist__games.append(game)
                    scm.session.commit()
                    print(f"Game '{game._Game__game_title}' added to wishlist for user '{user._User__username}'.")
                else:
                    print("User or game not found.")
            except Exception as e:
                print(f"Error adding game to wishlist: {str(e)}")
            finally:
                scm.session.close()

    def remove_wish_game(self, user, game):
        with self._session_cm as scm:
            try:
                user_ = scm.session.query(User).filter(func.lower(User._User__username) == func.lower(user.username)).first()
                game_ = scm.session.query(Game).filter(Game._Game__game_id == game.game_id).first()
                if user_ and game_:
                    user_._User__wishlist._Wishlist__games.remove(game)
                    scm.session.commit()
                    print(f"Game '{game._Game__game_title}' removed from wishlist for user '{user_._User__username}'.")
                else:
                    print("User or game not found.")
            except Exception as e:
                print(f"Error removing game from wishlist: {str(e)}")
            finally:
                scm.session.close()

    def get_wishlist(self, user):
        with self._session_cm as scm:
            try:
                user_ = scm.session.query(User).filter(func.lower(User._User__username) == func.lower(user.username)).first()

                if user_:
                    wishlist_games = user_._User__wishlist._Wishlist__games
                    # wishlist_titles = [game._Game__game_title for game in wishlist_games]
                    # print(f"Wishlist for user '{user._User__username}': {wishlist_titles}")
                    # if wishlist_games is None:
                    #     return []
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
        with self._session_cm as scm:
            try:
                # Query the user and game
                user_ = scm.session.query(User).filter(func.lower(User._User__username) == func.lower(user.username)).first()
                game_ = scm.session.query(Game).filter(Game._Game__game_id == game.game_id).first()

                if user_ and game_:
                    # Create a new Review instance
                    new_review = Review(
                        user_,
                        game_,
                        rating,
                        review_text,
                    )
                    print(new_review)
                    # Add the new review to the session
                    scm.session.add(new_review)
                    scm.session.commit()

                    print(f"Review added for game '{game._Game__game_title}' by user '{user._User__username}'.")
                else:
                    print("User or game not found.")
            except Exception as e:
                print(f"Error adding review to game: {str(e)}")
                scm.session.rollback()
            finally:
                scm.session.close()

    def get_user_review(self, user):
        with self._session_cm as scm:
            # Query the user by username
            user = scm.session.query(User).filter(func.lower(User._User__username) == func.lower(user.username)).first()

            if user:
                # Load the reviews relationship
                user_with_reviews = scm.session.query(User).options(orm.joinedload('reviews')).get(user.id)
                return user_with_reviews.reviews
            else:
                # User not found
                return None
