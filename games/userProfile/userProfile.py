from flask import Blueprint, render_template, session, redirect, flash, url_for, request
from flask_paginate import get_page_args, Pagination
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

# from flask_login import login_required

import games.adapters.repository as repo
from games.authentication.authentication import WishlistForm, login_required
from games.gameLibrary import services as gameservice
from games.authentication import services as authservice

from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres
from games.userProfile.services import remove_game_from_wishlist, add_game_to_wishlist, get_user_wishlist

userProfile_blueprint = Blueprint('pp_bp', __name__)


# @userProfile_blueprint.route('/userprofile', methods=['GET'])
# def view_user_profile():
#     genres = get_genres(repo.repo_instance)
#     all_games = services.get_games(repo.repo_instance)
#     return render_template('userProfile.html', all_genres=genres,
#                            genre_urls=get_genres_and_urls(), games=all_games)

@userProfile_blueprint.route('/userprofile', methods=['GET'])
@login_required  # You may use this decorator to ensure the user is logged in.
def view_user_profile():
    if 'username' in session:
        genres = get_genres(repo.repo_instance)
        all_games = gameservice.get_games(repo.repo_instance)
        user = authservice.get_user(session['username'], repo.repo_instance)
        wishlist = get_user_wishlist(user)
        page, per_page, offset = get_page_args(per_page_parameter="pp", pp=10)
        rendered = wishlist[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, offset=offset,
                                total=len(wishlist),
                                record_name='List')
        return render_template('userProfile.html', all_genres=genres,
                               genre_urls=get_genres_and_urls(),
                               games=all_games, user=user, wishlist=rendered, pagination=pagination)
    flash('Please login to access your profile', 'error')
    return redirect(url_for('viewGames_bp.view_games'))


# userProfile.py

# @userProfile_blueprint.route('/add_to_wishlist', methods=['POST'])
@userProfile_blueprint.route('/add_to_wishlist/<int:game_id>', methods=['POST'])
@login_required  # Ensure the user is logged in
def add_to_wishlist(game_id):
    user = authservice.get_user(session['username'], repo.repo_instance)
    form = WishlistForm()
    if form.validate_on_submit():
        # game_id = int(form.game_id.data)
        # game_id = int(request.form.get('game_id'))
        # game_id = 12460
        game = repo.repo_instance.get_games_by_id(game_id)

        if game:
            add_game_to_wishlist(user, game)
        else:
            flash('Game not found', 'error')
    return redirect(url_for('pp_bp.view_user_profile'))


@userProfile_blueprint.route('/remove_from_wishlist/<int:game_id>', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def remove_from_wishlist(game_id):
    user = authservice.get_user(session['username'], repo.repo_instance)
    game = repo.repo_instance.get_games_by_id(game_id)

    if game:
        remove_game_from_wishlist(user, game)
        return redirect(url_for('pp_bp.view_user_profile'))
    else:
        flash('Game not found', 'error')
        return redirect(url_for('pp_bp.view_user_profile'))
