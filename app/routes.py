from flask import render_template, flash, redirect, url_for
from app import app, db
from  app.models import User, Playlist, Song
from app.forms import LoginForm

user = {'username': ''}


@app.route('/index')
def index():
    if len(user) < 1:
        return redirect('/login')
    songs = []
    for song in Song.objects:
        songs.append(song)
    return render_template('index.html', title='Home', user=user, songs=songs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #flash('Login requested for user {}, remember_me={}'.format(
         #   form.username.data, form.remember_me.data))
        user['username'] = form.username.data
        return redirect('/index')
    return render_template('login.html', title='Sign In', user=user, form=form)

'''
$ export FLASK_APP=MDJ.py
$ flask run
'''