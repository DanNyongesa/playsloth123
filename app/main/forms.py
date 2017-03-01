from flask_wtf import Form
from wtforms import StringField, SubmitField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired
from .. import photos

class AlbumForm(Form):
    title = StringField("Album title")
    artist = StringField("Artist's name")
    genre = StringField("Genre")
    logo = FileField("Upload a logo for your album", validators=[FileRequired(), FileAllowed(photos, 'Can only upload photos!')])
    submit = SubmitField('Submit')


class SongForm(Form):
    title = StringField("Enter song title")
    song = StringField("upload song")
    submit = SubmitField('Submit')

