from flask import Blueprint, render_template, request, url_for
import games.adapters.repository as repo
from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres
from games.homepage import services
from flask_paginate import Pagination, get_page_args

search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search_games():
    search = request.args.get('query').strip()
    criteria = request.args.get('search_criteria')
    genres = get_genres(repo.repo_instance)
    if search:
        search_results = services.search_games_by_criteria(search, criteria,
                                                           repo.repo_instance)
        page, per_page, offset = get_page_args(per_page_parameter="pp", pp=10)
        pagination = Pagination(page=page, per_page=per_page, offset=offset,
                                total=len(search_results),
                                record_name='List')
        return render_template('searchResults.html', heading='Search Results',
                               games=search_results[offset: offset + per_page], all_genres=genres,
                               genre_urls=get_genres_and_urls(), pagination=pagination)
    else:
        return render_template('index.html', all_genres=genres,
                               genre_urls=get_genres_and_urls())
