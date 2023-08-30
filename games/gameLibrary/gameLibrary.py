import random

from flask import Blueprint, render_template, request, url_for
from flask_paginate import Pagination, get_page_args

import games.adapters.repository as repo
from games.gameLibrary import services

gameLibrary_blueprint = Blueprint('viewGames_bp', __name__)


@gameLibrary_blueprint.route('/gamelibrary', methods=['GET', 'POST'])
def view_games():
    sort_criteria = request.args.get('sort_criteria', 'title')  # Default sorting by title
    game_count = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    # slide_games = services.get_slide_games(repo.repo_instance)
    genres = services.get_genres(repo.repo_instance)

    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args(per_page_parameter="pp", pp=10)
    # rendered = selected_genre_games[((page-1)*per_page): ((page-1)*per_page + 5)]
    rendered = all_games[offset: offset + per_page]
    sorted_rendered = sorted(rendered, key=lambda x: x[sort_criteria])
    random_game_index = random.randrange(0, len(all_games) - 5)
    pagination = Pagination(page=page, per_page=per_page, offset=offset,
                            total=len(all_games),
                            record_name='List')
    return render_template('gameLibrary.html', heading='All Games',
                           games=sorted_rendered, num_games=game_count,
                           slide_games=all_games[random_game_index:random_game_index + 5], all_genres=genres,
                           pagination=pagination,
                           genre_urls=get_genres_and_urls())


def get_genres_and_urls(sort_criteria='title'):
    genre_names = services.get_genres(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('viewGames_bp.games_by_genre',
                                         genre=genre_name, sort_criteria=sort_criteria)
    return genre_urls


@gameLibrary_blueprint.route('/games_by_genre', methods=['GET', 'POST'])
def games_by_genre():
    # Read url parameters assuming at least one game with that genre
    target_genre = request.args.get('genre')
    sort_criteria = request.args.get('sort_criteria', 'title')
    selected_genre_games = services.get_games_by_genre(target_genre,
                                                       repo.repo_instance)
    # get_page_arg defaults to page 1, per_page of 10
    page, per_page, offset = get_page_args(per_page_parameter="pp", pp=10)
    # rendered = selected_genre_games[((page-1)*per_page): ((page-1)*per_page + 5)]
    rendered = selected_genre_games[offset: offset + per_page]
    sorted_rendered = sorted(rendered, key=lambda x: x[sort_criteria])
    pagination = Pagination(page=page, per_page=per_page, offset=offset,
                            total=len(selected_genre_games),
                            record_name='List')

    if len(selected_genre_games) < 5:
        slide_genre_games = selected_genre_games
    elif len(selected_genre_games) < 10:
        slide_genre_games = selected_genre_games[2:7]
    else:
        slide_genre_games = selected_genre_games[10:15]
    genres = services.get_genres(repo.repo_instance)
    return render_template('gameLibraryG.html', heading=target_genre,
                           games=sorted_rendered, all_genres=genres,
                           genre_urls=get_genres_and_urls(sort_criteria),
                           pagination=pagination,
                           slide_genre_games=slide_genre_games)


def side_bar_genres():
    genres = services.get_genres(repo.repo_instance)
    return render_template('sidebar.html', all_genres=genres,
                           genre_urls=get_genres_and_urls())