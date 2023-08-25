from flask import Blueprint, render_template
import games.adapters.repository as repo
import games.gamesDescription.services as services
from markupsafe import escape

games_description_blueprint = Blueprint('games_description_bp', __name__)

@games_description_blueprint.route('/games-description/<int:game_id>', methods=['GET'])
def games_description(game_id):
    get_game = services.get_game(repo.repo_instance, game_id)
    #get_game = services.get_game(repo.repo_instance)
    return render_template('gameDesc.html', game=get_game)



