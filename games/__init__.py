"""Initialize Flask app."""

from flask import Flask, render_template

import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository

# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from games.domainmodel.model import *


# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_game():
    some_game = Game(1, "Call of Duty® 4: Modern Warfare®")
    some_game.release_date = "Nov 12, 2007"
    some_game.price = 9.99
    some_game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of " \
                            "the Call of Duty® series, delivers the most intense and cinematic action experience ever. "
    some_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    return some_game


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    with app.app_context():
        from .gameLibrary import gameLibrary
        from .gamesDescription import gamesDescription
        from .homepage import search
        app.register_blueprint(gameLibrary.gameLibrary_blueprint)
        app.register_blueprint(gamesDescription.games_description_blueprint)
        app.register_blueprint(search.search_blueprint)

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)

    @app.route('/')
    def home():
        return render_template('index.html')

    return app
