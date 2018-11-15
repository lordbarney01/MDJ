from flask import render_template, flash, redirect, url_for, request, Blueprint
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, login_required, logout_user
from app.entities.models import User, Playlist, Song, load_user
from app.api.forms import LoginForm, RegistrationForm
from datetime import datetime

app = Blueprint('gui-routes', __name__)


@app.route('/playlist', methods=['GET', 'POST'])
@login_required
def playlists():
    if request.method == 'GET':
        user_playlists = load_user(current_user.userName).playlists
        if len(user_playlists) < 1:
            flash("There are no playlists for this user")
            return render_template('playlists.html', title='Playlists', playlists="")
        else:
            user_playlists_to_send = {}
            for playlist in user_playlists:
                playlist_songs = {}
                in_playlist = Playlist.objects.get(id=playlist.id)
                for song in in_playlist.songs:
                    song_to_add = Song.objects.get(id=song.id)
                    playlist_songs[song_to_add.songName] = song_to_add.youtubeUrl
                user_playlists_to_send[playlist.title] = playlist_songs
            return render_template('playlists.html', title='Playlists', playlists=user_playlists_to_send)


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        songs = []
        for song in Song.objects:
            songs.append(song)
        return render_template('index.html', title='Home', user=current_user, songs=songs)
    else:
        songs_for_playlist = request.form.getlist('song')
        songs_to_add = []
        for song in songs_for_playlist:
            song = Song.objects.get(youtubeUrl=song)
            songs_to_add.append(song)
        playlist = Playlist(title=current_user.userName + "_playlist_" + datetime.now().__str__(), songs=songs_to_add)
        playlist.save()
        user = load_user(current_user.userName)
        user.playlists.append(playlist)
        user.save()
        return redirect(url_for('gui-routes.playlists'))

        #user = load_user(current_user.userName)
        #user.playlists.append(playlist).save()
        #user.save()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(userName=form.username.data).first()
        if user is not None and len(user.userName) > 1:
            user = load_user(user.userName)
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('gui-routes.index')
            return redirect(next_page)
        return redirect(url_for('gui-routes.register'))
    return render_template('login.html', title='Sign In', user=current_user, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(userName=form.username.data)
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('gui-routes.login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('gui-routes.login'))
'''
$ export FLASK_APP=MDJ.py
$ flask run
'''