from flask import render_template, flash, redirect, url_for, jsonify, request, send_from_directory, current_app, abort
from . import main
from .. import db, photos, audio
from .forms import AlbumForm, SongForm
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
        flash("Album {} added".format(album_title))
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


@main.route("/songs/create/<int:album_id>", methods=['POST', 'GET'])
def add_song(album_id):
    form = SongForm()
    album = Album.query.filter_by(id=album_id).first_or_404()
    songs = Song.query.filter_by(album_id=album.id).all()
    if form.validate_on_submit():
        song_filename = audio.save(request.files['audio'])
        song_url = audio.url(song_filename)
        song_title = form.title.data
        song = Song(song_title=song_title,audio_url=song_url, audio_file=song_filename,album_id=album.id)
        db.session.add(song)
        db.session.commit()
        flash("[song] {} added".format(song_title))
        return redirect(url_for('main.detail',album_id=album.id))
    else:
        flash_errors(form)
    return render_template('add_song.html', form=form, album=album)


@main.route("/albums/detail/<int:album_id>")
def detail(album_id):
    album = Album.query.filter_by(id=album_id).first_or_404()
    songs = Song.query.filter_by(album_id=album.id).all()
    return render_template('details.html', album=album, songs=songs)


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

@main.route('/photos/<filename>')
def uploaded_image(filename):
    return send_from_directory(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], 'photos'), filename)


@main.route('/audio/<filename>')
def uploaded_song(filename):
    return send_from_directory(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], 'audio'), filename)



@main.route("/songs/delete/<int:album_id>/<int:song_id>", methods=['POST', 'GET'])
def delete_song(album_id, song_id):
    album = Album.query.filter_by(id=album_id).first_or_404()
    songs = Song.query.filter_by(album_id=album.id).all()
    song = filter(lambda song: song.id==song_id, songs)
    if len(song)>0:
        db.session.delete(song[0])
        db.session.commit()
        flash("Deleted ".format(song[0].song_title))
        return redirect(url_for('main.detail', album_id=album.id))
    abort(404)


@main.route("/songs/favourite/<int:song_id>")
def favourite_song(song_id):
    song = Song.query.filter_by(id=song_id).first_or_404()
    if song.is_favorite:
        song.is_favorite = False
    else:
        song.is_favorite = True
    db.session.add(song)
    db.session.commit()
    return redirect(url_for('main.detail', album_id=song.album_id))

# TODO
@main.route("/songs/<int:song_id>")
def get_song(song_id):
    pass

