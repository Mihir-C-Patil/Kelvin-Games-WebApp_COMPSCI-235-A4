"""Initialize Flask app."""

from flask import Flask, render_template

import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import *

def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    with app.app_context():
        from .homepage import search
        app.register_blueprint(search.search_blueprint)

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)

    @app.route('/')
    def home():
        return render_template('index.html')

    return app
