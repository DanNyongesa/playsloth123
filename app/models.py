from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    album = db.relationship('Album', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return "<User: %r>" % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # role verification
    def can(self, permissions):
        return self.role is not None and (self.role.permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    # check last seen
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False


class Album(db.Model):
    __tablename__= 'albums'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(250))
    album_title = db.Column(db.String(250))
    genre = db.Column(db.String(100))
    album_logo = db.Column(db.String(250), default='')
    logo_url = db.Column(db.String, default=None)
    is_favorite = db.Column(db.Boolean, default=False)
    song = db.relationship('Song', backref='album', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
         return self.album_title + ' -' + self.artist


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String)
    audio_file = db.Column(db.String, default='')
    audio_url = db.Column(db.String, default=None)
    is_favorite = db.Column(db.Boolean, default=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    def __str__(self):
         return str(self.song_title)

class Role(db.Model):
    __tablename_='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles={
            'User':(Permission.FOLLOW,Permission.FAVOURITE|Permission.UPLOAD, True),
            'Moderator':(Permission.FOLLOW,Permission.FAVOURITE|Permission.UPLOAD|Permission.MODERATE_UPLOADS, False),
            'Administrator':(0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.Permissions = roles[r][0]
            role.default = role[r][1]
            db.session.add(role)
        db.session.commit()

class Permission:
    FOLLOW = 0x01
    FAVOURITE=0x02
    UPLOAD=0x04
    MODERATE_UPLOADS = 0x08
    ADMINISTER=0x80

