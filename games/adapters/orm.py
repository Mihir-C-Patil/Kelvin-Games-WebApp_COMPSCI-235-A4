from sqlalchemy import (Table, MetaData, Column, Integer, String, Date,
                        DateTime, ForeignKey, JSON)

from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import *

metadata = MetaData()

users_table = Table('user', metadata,
                    Column('id', Integer, primary_key=True,
                           autoincrement=True),
                    Column('username', String(255), unique=True,
                           nullable=False),
                    Column('password', String(255), nullable=False),
                    Column('wishlist_id', ForeignKey('wishlist.id')),
                    Column('reviews', ForeignKey('review.id')))

games_table = Table('game', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('game_title', String(255), nullable=False),
                    Column('price', Integer, nullable=False),
                    Column('release_date', String(15), nullable=False),
                    Column('description', String(1024)),
                    Column('publisher', ForeignKey('publisher.publisher_name')),
                    Column('image_url', String(1024), nullable=False),
                    Column('website_url', String(1024)),
                    Column('video_url', String(1024)),
                    Column('tags', String(1024), nullable=False),
                    Column('system_dict', JSON), )

genres_table = Table('genre', metadata,
                     Column('genre_name', String(255), nullable=False, primary_key=True))

game_genres_table = Table('game_genres', metadata,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('game_id', ForeignKey('game.id')),
                          Column('genre_name', ForeignKey('genre.genre_name')))

publishers_table = Table('publisher', metadata,
                         Column('publisher_name', String(255), nullable=False, primary_key=True))

reviews_table = Table('review', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user', ForeignKey('user.id')),
                      Column('game', ForeignKey('game.id')),
                      Column('rating', Integer, nullable=False),
                      Column('comment', String(1024), nullable=False),
                      Column('timestamp', String(30), nullable=False))

wishlists_table = Table('wishlist', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user', ForeignKey('user.id')))

wishlist_games_table = Table('wishlist_games', metadata,
                             Column('id', Integer, primary_key=True, autoincrement=True),
                             Column('wishlist_id', ForeignKey('wishlist.id')),
                             Column('game_id', ForeignKey('game.id')))


# class GameGenre:
#     def __init__(self, game_id, genre_name):
#         self.game_id = game_id
#         self.genre_name = genre_name


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, foreign_keys=[reviews_table.c.user]),
        '_User__wishlist': relationship(Wishlist, foreign_keys=[wishlists_table.c.user],
                                        back_populates='_Wishlist__user', uselist=False),
        '_User__wishlist_id': users_table.c.wishlist_id
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.description,
        '_Game__publisher': relationship(Publisher, foreign_keys=[games_table.c.publisher],
                                         back_populates='_Publisher__games'),
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__video_url': games_table.c.video_url,
        '_Game__tags_string': games_table.c.tags,
        '_Game__publisher_id': games_table.c.publisher,
        '_Game__system_dict': games_table.c.system_dict,
        '_Game__genres': relationship(Genre, secondary=game_genres_table, back_populates='_Genre__games'),
        '_Game__wishlist': relationship(Wishlist, secondary=wishlist_games_table, back_populates='_Wishlist__games'),
        '_Game__reviews': relationship(Review, back_populates='_Review__game')
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
        '_Genre__games': relationship(Game, secondary=game_genres_table, back_populates='_Game__genres')
    })

    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.publisher_name,
        '_Publisher__games': relationship(Game, foreign_keys=[games_table.c.publisher],
                                          back_populates='_Game__publisher')
    })

    mapper(Review, reviews_table, properties={
        '_Review__comment': reviews_table.c.comment,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__game_id': reviews_table.c.game,
        '_Review__user_id': reviews_table.c.user,
        '_Review__game': relationship(Game, foreign_keys=[reviews_table.c.game], back_populates='_Game__reviews'),
        '_Review__user': relationship(User, foreign_keys=[reviews_table.c.user], back_populates='_User__reviews')
    })

    mapper(Wishlist, wishlists_table, properties={
        '_Wishlist__games': relationship(Game, secondary=wishlist_games_table, back_populates='_Game__wishlist'),
        '_Wishlist__user': relationship(User, foreign_keys=[wishlists_table.c.user], back_populates='_User__wishlist')
    })

    # mapper(GameGenre, game_genres_table, properties={
    #     '_GameGenre__game': relationship(Game, back_populates='_GameGenre__games'),
    #     '_GameGenre__genre': relationship(Genre, back_populates='_GameGenre__genre')
    # })
