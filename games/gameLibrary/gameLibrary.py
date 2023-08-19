from flask import Blueprint, render_template

from games.gameLibrary import services
import games.adapters.repository as repo

gameLibrary_blueprint = Blueprint('viewGames_bp', __name__)


@gameLibrary_blueprint.route('/gamelibrary', methods=['GET'])
def view_games():
    game_count = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    return render_template('gameLibrary.html', heading='All Games', games=all_games, num_games=game_count)
