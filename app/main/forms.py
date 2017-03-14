from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired
from .. import photos, audio

class AlbumForm(Form):
    title = StringField("Album title")
    artist = StringField("Artist's name")
    genre = StringField("Genre")
    logo = FileField("Upload a logo for your album", validators=[FileRequired(), FileAllowed(photos, 'Can only upload photos!')])
    submit = SubmitField('Submit')


class SongForm(Form):
    title = StringField("Enter song title")
    audio = FileField("Upload song", validators=[FileRequired(), FileAllowed(audio, 'Can only upload photos!')])
    submit = SubmitField('Submit')

