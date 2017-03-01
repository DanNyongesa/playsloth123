from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app(configname):
    app = Flask(__name__)
    app.config.from_object(config[configname])
    bootstrap.init_app(app)
    db.init_app(app)

    # main blueprint
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # auth blueprint
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app