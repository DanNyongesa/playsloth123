from . import main
from flask import render_template


@main.app_errorhandler(404)
def not_found(error):
    return render_template('main/404.html'), 404


@main.app_errorhandler(400)
def not_found(error):
    return render_template('main/400.html'), 400


@main.app_errorhandler(405)
def not_found(error):
    return render_template('main/405.html'), 405
