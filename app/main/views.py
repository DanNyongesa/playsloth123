from flask import render_template, flash, redirect, url_for, jsonify, request, send_from_directory, current_app
from . import main
from .. import db, photos
from .forms import AlbumForm
from ..models import Album, Song
from .. import db
from werkzeug.utils import secure_filename
import os


@main.route("/")
@main.route("/home")
def index():
    albums = Album.query.all()
    return render_template("index.html", albums=albums)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@main.route("/albums/add", methods=['GET', 'POST'])
def add_album():
    form = AlbumForm()
    if form.validate_on_submit():
        filename = photos.save(request.files['logo'])
        url = photos.url(filename)
        artist = form.artist.data
        album_title = form.title.data
        genre = form.genre.data
        album = Album(artist=artist, album_title=album_title, genre=genre,album_logo=filename,logo_url=url)
        db.session.add(album)
        db.session.commit()
        flash("Album added at {}".format(filename))
        return redirect(url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('add_album.html', form=form)


@main.route("/albums/delete/<int:album_id>", methods=['DELETE', 'POST'])
def delete_album(album_id):
    album = Album.query.filter_by(id=album_id).first_or_404()
    db.session.delete(album)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route("/albums/<int:album_id>")
def get_album(album_id):
    album = Album.query.filter_by(id=album_id).first_or_404()
    songs = Song.query.filter_by(album_id=album.id).all()
    return render_template('detail.html', album=album, songs=songs)


@main.route("/songs/create")
def add_song():
    pass


@main.route("/songs/delete/<int:album_id>/<int:song_id>")
def delete_song(album_id, song_id):
    album = Album.query.filter_by(album_id=album_id).first_or_404()
    # song = Song.query.filter_by(album_id=)


@main.route("/songs/<int:song_id>")
def get_song(song_id):
    pass

@main.route('/uploads/<filename>')
def uploaded_image(filename):
    return send_from_directory(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], 'photos'), filename)

@main.route("/songs")
def get_songs():
    pass


@main.route("/albums/detail/<int:album_id>")
def detail(album_id):
    album = Album.query.filter_by(id=album_id).first_or_404()
    return render_template('details.html', album=album)


@main.route("/songs/favourite/<int:song_id>")
def favourite_song(song_id):
    song = Song.query.filter_by(id=song_id).first_or_404()
    song.is_favorite = True
    db.session.add(song)
    db.session.commit()
    pass


@main.route("/albums/favourite", methods=['POST', 'GET'])
def favourite_album():
    album_id = request.json.get('id')
    album = Album.query.filter_by(id=album_id).first_or_404()
    if album.is_favorite:
        album.is_favorite = False
    else:
        album.is_favorite = True
    db.session.add(album)
    db.session.commit()
    resp = jsonify({'message': "Success", "value": album.is_favorite})
    resp.status_code = 200
    return resp
