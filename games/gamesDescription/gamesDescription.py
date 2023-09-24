from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from better_profanity import Profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from games.authentication.authentication import login_required
import games.adapters.repository as repo
import games.gamesDescription.services as services
from games.authentication import services as authservice
from datetime import datetime
from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres
from flask_paginate import Pagination, get_page_args
import random

from games.userProfile.services import get_user_wishlist, get_user_wishlist_objs


class ReviewForm(FlaskForm):
    """
    A form for users to submit game reviews.

    Attributes:
        rating (SelectField): The rating of the game, with options from
        1 to 5 stars.
        comment (TextAreaField): The user's review comment.
        submit (SubmitField): A button to submit the review.

    """
    options = [(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')]
    rating = SelectField('Rating', choices=options, coerce=int)
    comment = TextAreaField('Review', [DataRequired()])
    # game_id = HiddenField('game_id')
    submit = SubmitField('Submit Review')
    # game_id = HiddenField("Game id")


games_description_blueprint = Blueprint('games_description_bp', __name__)


@games_description_blueprint.route('/games-description/<int:game_id>',
                                   methods=['GET'])
def games_description(game_id):
    """
    This method is used to display the description of a game and additional
     information such as similar games, reviews, and genres.

    Parameters:
    - game_id (int): The ID of the game to display the description for.

    Returns:
    - render_template: The rendered game description page.

    Example Usage:
    games_description(1)

    """
    get_game = services.get_game(repo.repo_instance, game_id)
    # get_similar_games = None
    if len(get_game.genres) > 0:
        get_similar_games = services.similar_game(repo.repo_instance,
                                                  get_game.genres)
    reviews_copy = get_game.reviews[:]
    reviews_copy.reverse()
    genres = get_genres(repo.repo_instance)
    form = ReviewForm()
    get_average = services.get_average(get_game)
    get_number_of_reviews = len(get_game.reviews)
    page, per_page, offset = get_page_args(per_page_parameter="pp", pp=2)
    rendered = reviews_copy[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, offset=offset,
                            total=len(get_game.reviews),
                            record_name='List')
    if 'username' in session and authservice.get_user(session['username'], repo.repo_instance) is not None:
        user = authservice.get_user(session['username'], repo.repo_instance)
        wishlist = get_user_wishlist_objs(user)
    else:
        wishlist = []
    # print(wishlist)
    return render_template('gameDesc.html', game=get_game,
                           similar_games=[game for game in get_similar_games
                                          if game != get_game][0:4],
                           all_genres=genres,
                           genre_urls=get_genres_and_urls(), form=form, average=get_average,
                           review_number=get_number_of_reviews, pagination=pagination, page_reviews=rendered,
                           wishlist=wishlist)


@games_description_blueprint.route('/review/<int:game_id>', methods=['POST'])
@login_required
def post_review(game_id):
    """
    Publishes a review for a game.

    Parameters:
        game_id (int): The ID of the game to post the review for.

    Returns:
        None
    """
    game = services.get_game(repo.repo_instance, game_id)
    form = ReviewForm()
    if 'username' in session:
        user = authservice.get_user(session['username'], repo.repo_instance)
        if form.validate_on_submit():
            timestamp = datetime.utcnow().strftime("%d %B %Y %I:%M:%S")
            if services.add_review(form.rating.data, form.comment.data, user, game):
                flash('Review successfully added', 'success')
                return redirect(url_for('games_description_bp'
                                        '.games_description', game_id=game_id))
            else:
                flash('You have already added a review for this game!',
                      'error')
                return redirect(url_for('games_description_bp'
                                        '.games_description', game_id=game_id))
        else:
            flash('Form validation failed. Please try again!', 'error')
            return redirect(url_for('games_description_bp.games_description',
                                    game_id=game_id))
