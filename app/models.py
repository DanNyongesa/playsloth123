from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(20))
    # album = db.relationship('Album', backref='user', lazy='dynamic')
    def __repr__(self):
        return "<User: %r>" % self.name


class Album(db.Model):
    __tablename__= 'albums'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(250))
    album_title = db.Column(db.String(250))
    genre = db.Column(db.String(100))
    album_logo = db.Column(db.LargeBinary, default='')
    is_favorite = db.Column(db.Boolean, default=False)
    song = db.relationship('Song', backref='album', lazy='dynamic')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
         return "<%r - %r>" % (self.album_title, self.artist)


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String(250))
    audio_file = db.Column(db.LargeBinary, default='')
    is_favorite = db.Column(db.Boolean, default=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    def __repr__(self):
         return "<Song: %r>" % self.song_title