from flask_wtf import Form
from wtforms import StringField, FileField, SubmitField


class AlbumForm(Form):
    title = StringField("Enter album title")
    artist = StringField("Enter artist's name")
    genre = StringField("Whats the genre")
    logo = FileField("Upload a logo for your album")
    submit = SubmitField('Submit')


class SongForm(Form):
    title = StringField("Enter song title")
    song = StringField("upload song")
    submit = SubmitField('Submit')

