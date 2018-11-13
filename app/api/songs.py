from lxml import etree
from app.api import bp
from app.entities.models import Song
from app.api.erros import bad_request
from flask import jsonify
from app.tasks.tasks import TaskAddSong, TaskDeleteSong
import urllib

@bp.route('/songs/<youtubeUrl>', methods=['POST'])
def add_song(youtubeUrl):
    youtube = etree.HTML(urllib.request.urlopen("http://www.youtube.com/watch?v=" + youtubeUrl).read())
    video_title = str(youtube.xpath("//span[@id='eow-title']/@title"))[2:-2]
    if len(video_title) < 2:
        return bad_request("url for song incorrect")
    try:
        TaskAddSong().run(youtubeUrl=youtubeUrl, songName=video_title)
    except RuntimeError:
        return bad_request("song already exists")
    response = jsonify()
    response.status_code = 201

    return response


@bp.route('/songs/<youtubeUrl>', methods=['DELETE'])
def delete_song(youtubeUrl):
    try:
        TaskDeleteSong().run(youtubeUrl=youtubeUrl)
    except RuntimeError:
        return bad_request("url for song incorrect or this song does not exist")
    response = jsonify()
    response.status_code = 204

    return response

@bp.route('/songs/', methods=['GET'])
def get_songs():
    data = {}

    for song in Song.objects():
        data[song.youtubeUrl] = song.to_json()

    return jsonify(data)
