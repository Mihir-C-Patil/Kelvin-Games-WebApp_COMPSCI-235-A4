from flask import Blueprint, render_template, request, url_for

from games.gameLibrary import services
import games.adapters.repository as repo

gameLibrary_blueprint = Blueprint('viewGames_bp', __name__)


@gameLibrary_blueprint.route('/gamelibrary', methods=['GET'])
def view_games():
    game_count = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    slide_games = services.get_slide_games(repo.repo_instance)
    genres = services.get_genres(repo.repo_instance)
    return render_template('gameLibrary.html', heading='All Games', games=all_games, num_games=game_count,
                           slide_games=slide_games, all_genres=genres)


def get_genres_and_urls():
    genre_names = services.get_genres(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('viewGames_bp.games_by_genre', genre=genre_name)
    return genre_urls


@gameLibrary_blueprint.route('/games_by_genre', methods=['GET'])
def games_by_genre():
    # Read url parameters assuming there will be at least one game with that genre
    target_genre = request.args.get('genre')
    selected_genre_games = services.get_games_by_genre(target_genre, repo.repo_instance)
    for genre in selected_genre_games:
        genre['game_genre_url'] = url_for('viewGames_bp.games_by_genre', genre=target_genre)
    # genre_url = url_for('viewGames_bp.games_by_genre', genre=target_genre)
    genres = services.get_genres(repo.repo_instance)
    return render_template('gameLibraryG.html', heading=target_genre, games=selected_genre_games, all_genres=genres,
                           genre_urls=get_genres_and_urls())
