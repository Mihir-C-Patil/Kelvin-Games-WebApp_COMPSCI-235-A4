"""Initialize Flask app."""

from flask import Flask, render_template
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo
from games.adapters import database_repository, populate_database, memory_repository
from games.adapters.orm import metadata, map_model_to_tables
from games.adapters.populate_database import GameFileCSVReader
from games.adapters.memory_repository import MemoryRepository
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
    data_path = Path('games') / 'adapters' / 'data' / 'games.csv'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
        repo.repo_instance = MemoryRepository()

    if app.config['REPOSITORY'] == 'MEMORY':
        repo.repo_instance = memory_repository.MemoryRepository()
        database_mode = False
        reader = GameFileCSVReader(data_path, repo.repo_instance,
                                   database_mode)
        reader.read_csv_file()

    if app.config['REPOSITORY'] == 'DATABASE':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri,
                                        connect_args={"check_same_thread":
                                                          False},
                                        poolclass=NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True,
                                       bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' \
                or len(database_engine.table_names()) == 0:
            print('Repopulating database...')
            print('Please wait...')
            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())

            map_model_to_tables()

            database_mode = True
            reader = GameFileCSVReader(data_path, repo.repo_instance,
                                       database_mode)
            reader.read_csv_file()
            print('Repopulating Finished!')

        else:
            map_model_to_tables()

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

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

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
