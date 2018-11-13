from mongoengine import Document, StringField, DateTimeField, ListField, BooleanField, ReferenceField
from flask_login import UserMixin
from app import login


class Song(Document):
    youtubeUrl = StringField(unique=True, required=True)
    songName = StringField(required=True, max_length=100, min_length=1)
    genre = ListField(StringField())
    author = StringField()


class Playlist(Document):
    title = StringField(unique=True, required=True)
    isPrivate = BooleanField()
    songs = ListField(ReferenceField(Song))


    #ef __init__(self, title, songs):
    #   super(Playlist, Playlist).__init__(self)
    #   self.title = title
    #   for song in songs:
    #       self.songs.append(Song(youtubeUrl=song.youtubeUrl))



class User(UserMixin, Document):
    userName = StringField(unique=True, required=True, max_length=20, min_length=2)
    playlists = ListField(ReferenceField(Playlist))


@login.user_loader
def load_user(username):
    try:
        return User.objects.get(userName=username)
    except:
        return User.objects.get(userName='bbb')


