from flask import Blueprint, render_template
import games.adapters.repository as repo
from games.gameLibrary import services

from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres

userProfile_blueprint = Blueprint('pp_bp', __name__)


@userProfile_blueprint.route('/userprofile', methods=['GET'])
def view_user_profile():
    genres = get_genres(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    return render_template('userProfile.html', all_genres=genres,
                           genre_urls=get_genres_and_urls(), games=all_games)
