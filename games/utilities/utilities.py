from flask import Blueprint, request, render_template, redirect, url_for, \
    session

import games.adapters.repository as repo
import games.utilities.services as services

utilities_blueprint = Blueprint('utilities_bp', __name__)

