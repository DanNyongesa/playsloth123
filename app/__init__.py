from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_uploads import configure_uploads, UploadSet, IMAGES, AUDIO
from flask_login import LoginManager
import sys

if sys.version_info >= (3,0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy

csrf = CSRFProtect()
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos', IMAGES)
audio = UploadSet('audio', AUDIO)

def create_app(configname):
    app = Flask(__name__)
    login_manager.init_app(app)
    app.config.from_object(config[configname])
    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    configure_uploads(app, (photos, audio))

    # main blueprint
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # auth blueprint
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    #index searches
    from .models import Song, Album
    if enable_search:
        flask_whooshalchemy.whoosh_index(app, Song)
        flask_whooshalchemy.whoosh_index(app, Album)

    return app