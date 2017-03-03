from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    album = db.relationship('Album', backref='user', lazy='dynamic')

    def __str__(self):
        return "User: %s" % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Album(db.Model):
    __tablename__= 'albums'
    __searchable__ = ['artist', 'album_title']
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(250))
    album_title = db.Column(db.String(250))
    genre = db.Column(db.String(100))
    album_logo = db.Column(db.String(250), default='')
    logo_url = db.Column(db.String, default=None)
    is_favorite = db.Column(db.Boolean, default=False)
    song = db.relationship('Song', backref='album', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
         return self.album_title + ' -' + self.artist


class Song(db.Model):
    __tablename__ = 'songs'
    __searchable__ = ['song_title']
    id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String)
    audio_file = db.Column(db.String, default='')
    audio_url = db.Column(db.String, default=None)
    is_favorite = db.Column(db.Boolean, default=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    def __str__(self):
         return str(self.song_title)


