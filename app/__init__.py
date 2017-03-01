from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_uploads import configure_uploads, UploadSet, IMAGES, AUDIO


csrf = CSRFProtect()
db = SQLAlchemy()
bootstrap = Bootstrap()

photos = UploadSet('photos', IMAGES)
audio = UploadSet('audio', AUDIO)

def create_app(configname):
    app = Flask(__name__)
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
    app.register_blueprint(auth_blueprint)

    return app