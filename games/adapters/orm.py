from sqlalchemy import (Table, MetaData, Column, Integer, String, Date,
                        DateTime, ForeignKey)

from sqlalchemy.orm import mapper, relationship, synonym

from games.domainmodel.model import *

metadata = MetaData()

users_table = Table('user', metadata,
                    Column('id', Integer, primary_key=True,
                           autoincrement=True),
                    Column('username', String(255), unique=True,
                           nullable=False),
                    Column('password', String(255), nullable=False),
                    Column('wishlist', ForeignKey('wishlist.id')),
                    Column('reviews', ForeignKey('review.id')))

games_table = Table('game', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('game_title', String(255), nullable=False),
                    Column('price', Integer, nullable=False),
                    Column('release_date', Date, nullable=False),
                    Column('description', String(1024), nullable=False),
                    Column('publisher', ForeignKey('publisher.id')),
                    Column('image_url', String(1024), nullable=False),
                    Column('website_url', String(1024), nullable=False),
                    Column('tags', String(1024), nullable=False))

genres_table = Table('genre', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('genre_name', String(255), nullable=False))

game_genres_table = Table('game_genres', metadata,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('game_id', ForeignKey('game.id')),
                          Column('genre_name', ForeignKey('genre.id')))

publishers_table = Table('publisher', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('publisher_name', String(255), nullable=False))

reviews_table = Table('review', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('review_text', String(1024), nullable=False),
                      Column('rating', Integer, nullable=False),
                      Column('timestamp', DateTime, nullable=False),
                      Column('game', ForeignKey('game.id')),
                      Column('user', ForeignKey('user.id')))

wishlists_table = Table('wishlist', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('games', ForeignKey('game.id')),
                        Column('user', ForeignKey('user.id')))


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, foreign_keys=[reviews_table.c.user]),
        '_User__wishlist': relationship(Wishlist, foreign_keys=[wishlists_table.c.user])
    })
    mapper(Game, games_table, properties={
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.description,
        '_Game__publisher': relationship(Publisher, foreign_keys=[games_table.c.publisher],
                                         back_populates='_Publisher__games'),
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__tags_string': games_table.c.tags
    })
    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name
    })
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.publisher_name,
        '_Publisher__games': relationship(Game, foreign_keys=[games_table.c.publisher],
                                          back_populates='_Game__publisher')
    })
    mapper(Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__game': relationship(Game),
        '_Review__user': relationship(User, foreign_keys=[reviews_table.c.user], back_populates='_User__reviews')
    })
    mapper(Wishlist, wishlists_table, properties={
        '_Wishlist__games': relationship(Game),
        '_Wishlist__user': relationship(User, foreign_keys=[wishlists_table.c.user], back_populates='_User__wishlist')
    })
