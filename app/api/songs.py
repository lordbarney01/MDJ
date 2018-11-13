from app.api import bp
from app.models import Song
from app.api.erros import bad_request
from flask import jsonify
from lxml import etree
import urllib


@bp.route('/songs/<youtubeUrl>', methods=['POST'])
def add_song(youtubeUrl):
    youtube = etree.HTML(urllib.request.urlopen("http://www.youtube.com/watch?v=" + youtubeUrl).read())
    video_title = str(youtube.xpath("//span[@id='eow-title']/@title"))[2:-2]
    if len(video_title) < 2:
        return bad_request("url for song incorrect")
    song = Song()
    song.youtubeUrl = youtubeUrl
    song.songName = video_title
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
