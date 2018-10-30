from  app.api import bp
from app.models import Song
from flask import url_for, request
from app.api.erros import bad_request
from flask import jsonify

@bp.route('/songs/', methods=['POST'])
def add_song(youtubeUrl):
    data = request.get_json() or {}
    if 'youtubeUrl' not in data or 'songName' not in data:
        return bad_request()
    song = Song()
    song.youtubeUrl = data['youtubeUrl']
    song.songName = data['songName']
    if 'author' in data:
        song.author = data['author']
    if 'genre' in data:
        song.genre = data['genre']

    song.save()
    response = jsonify()
    response.status_code = 201

    return response


@bp.route('/songs/', methods=['GET'])
def get_songs():
    data = {}

    for song in Song.objects():
        data[song.youtubeUrl] = song.to_json()

    return jsonify(data)