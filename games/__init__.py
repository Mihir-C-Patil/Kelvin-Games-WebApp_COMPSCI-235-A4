"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path

from flask.testing import FlaskClient

import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository
from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres

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


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

        def test_pagination(app: FlaskClient):
            with app:
                response = app.get('/gamelibrary')
                assert response.status_code == 200

                # Simulate pagination query parameters
                with app.get('/gamelibrary?page=2&pp=10', follow_redirects=True) as response:
                    assert response.status_code == 200

                # Test games_by_genre pagination
                with app.get('/games_by_genre?genre=Action', follow_redirects=True) as response:
                    assert response.status_code == 200

                # Simulate games_by_genre pagination query parameters
                with app.get('/games_by_genre?genre=Action&page=2&pp=10', follow_redirects=True) as response:
                    assert response.status_code == 200

    with app.app_context():
        from .gameLibrary import gameLibrary
        from .gamesDescription import gamesDescription
        from .homepage import search
        app.register_blueprint(gameLibrary.gameLibrary_blueprint)
        app.register_blueprint(gamesDescription.games_description_blueprint)
        app.register_blueprint(search.search_blueprint)

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    @app.route('/')
    def home():
        genres = get_genres(repo.repo_instance)
        return render_template('index.html', all_genres=genres,
                               genre_urls=get_genres_and_urls())

    return app
