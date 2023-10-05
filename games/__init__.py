"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo
from games.adapters import repository  # TODO: import database repo etc
from games.adapters.memory_repository import populate, MemoryRepository
from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres
from games.domainmodel.model import *


def create_app(test_config=None):
    """
    Creates and configures the Flask application.

    Parameters:
    -----------
    test_config : dict, optional
        Configuration dictionary to be used for testing purposes.

    Returns:
    --------
    app : Flask
        The Flask application object.

    Examples:
    ---------
    Create a Flask application object:
        app = create_app()

    Create a Flask application object with a test configuration:
        test_config = {'TESTING': True}
        app = create_app(test_config=test_config)
    """

    # Create the Flask app object.
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    with app.app_context():
        from .gameLibrary import gameLibrary
        from .gamesDescription import gamesDescription
        from .homepage import search
        from .userProfile import userProfile
        from .authentication import authentication
        app.register_blueprint(gameLibrary.gameLibrary_blueprint)
        app.register_blueprint(gamesDescription.games_description_blueprint)
        app.register_blueprint(search.search_blueprint)
        app.register_blueprint(userProfile.userProfile_blueprint)
        app.register_blueprint(authentication.authentication_blueprint)

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    @app.route('/')
    def home():
        """
        Renders the homepage of the web application.

        Returns:
            str: The rendered HTML template for the homepage.

        Usage:
            The `home` method is a Flask route decorator for the
            homepage URL or path ('/'). When a request is made to the
            homepage, this method is called, retrieves the genres from
            the repository, and renders the 'index.html' template with
            the available genres and their corresponding URLs.

        """
        genres = get_genres(repo.repo_instance)
        return render_template('index.html', all_genres=genres,
                               genre_urls=get_genres_and_urls())

    @app.route('/about')
    def about():
        """
        Renders the 'about' page of the application.

        Returns:
            str: The rendered HTML template of the 'about' page.

        """
        genres = get_genres(repo.repo_instance)
        return render_template('about.html', all_genres=genres,
                               genre_urls=get_genres_and_urls())

    return app
