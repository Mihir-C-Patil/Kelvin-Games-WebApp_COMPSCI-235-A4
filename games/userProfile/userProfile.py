from flask import Blueprint, render_template, session, redirect, flash, \
    url_for, request
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
from games.userProfile.services import (remove_game_from_wishlist,
                                        add_game_to_wishlist,
                                        get_user_wishlist,
                                        get_user_reviews)

userProfile_blueprint = Blueprint('pp_bp', __name__)


@userProfile_blueprint.route('/userprofile', methods=['GET'])
@login_required  # You may use this decorator to ensure the user is logged in.
def view_user_profile():
    """
    Displays the user profile page.

    Returns:
        The rendered user profile page.

    Exceptions:
        None
    """
    if 'username' in session:
        genres = get_genres(repo.repo_instance)
        all_games = gameservice.get_games(repo.repo_instance)
        user = authservice.get_user(session['username'], repo.repo_instance)
        wishlist = get_user_wishlist(user)
        page, per_page, offset = get_page_args(per_page_parameter="pp", pp=7)
        rendered = wishlist[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, offset=offset,
                                total=len(wishlist),
                                record_name='List')
        reviews = get_user_reviews(user)
        return render_template('userProfile.html', all_genres=genres,
                               genre_urls=get_genres_and_urls(),
                               games=all_games, user=user, wishlist=rendered,
                               pagination=pagination, reviews=reviews)
    flash('Please login to access your profile', 'error')
    return redirect(url_for('viewGames_bp.view_games'))


@userProfile_blueprint.route('/add_to_wishlist/<int:game_id>',
                             methods=['POST'])
@login_required  # Ensure the user is logged in
def add_to_wishlist(game_id):
    """
    Add a game to the user's wishlist.

    Parameters:
    - game_id (int): The ID of the game to be added to the wishlist.

    Returns:
    - None

    This method adds a game to the user's wishlist by getting the user
     from the session and validating the wishlist form. If the form is
     valid, the game with the"""
    user = authservice.get_user(session['username'], repo.repo_instance)
    form = WishlistForm()
    if form.validate_on_submit():

        game = repo.repo_instance.get_games_by_id(game_id)

        if game:
            add_game_to_wishlist(user, game)
        else:
            flash('Game not found', 'error')
    return redirect(url_for('pp_bp.view_user_profile'))


@userProfile_blueprint.route('/remove_from_wishlist/<int:game_id>',
                             methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def remove_from_wishlist(game_id):
    """

    Parameters:
    - game_id (int): The ID of the game to be removed from the user's
    wishlist.

    Returns:
    - Redirect: Redirects the user to the user profile page after
    removing the game from the wishlist.

    """
    user = authservice.get_user(session['username'], repo.repo_instance)
    game = repo.repo_instance.get_games_by_id(game_id)

    if game:
        remove_game_from_wishlist(user, game)
        return redirect(url_for('pp_bp.view_user_profile'))
    else:
        flash('Game not found', 'error')
        return redirect(url_for('pp_bp.view_user_profile'))
