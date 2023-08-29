from flask import Blueprint, render_template, request, url_for
import games.adapters.repository as repo
from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres
from games.homepage import services

search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search_games():
    search = request.args.get('query').strip()
    criteria = request.args.get('search_criteria')
    genres = get_genres(repo.repo_instance)
    if search:
        search_results = services.search_games_by_criteria(search, criteria,
                                                           repo.repo_instance)
        return render_template('searchResults.html', heading='Search Results',
                               games=search_results, all_genres=genres,
                               genre_urls=get_genres_and_urls())
    else:
        return render_template('index.html', all_genres=genres,
                               genre_urls=get_genres_and_urls())


def side_bar_genres():
    genres = get_genres(repo.repo_instance)
    return render_template('index.html', all_genres=genres,
                           genre_urls=get_genres_and_urls())
