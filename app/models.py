from mongoengine import Document, StringField, DateTimeField, ListField, BooleanField


class Song(Document):
    youtubeUrl = StringField(unique=True, required=True)
    songName = StringField(required=True, max_length=50, min_length=1)
    genre = ListField(StringField())
    author = StringField()


class Playlist(Document):
    title = StringField(unique=True, required=True)
    isPrivate = BooleanField()
    songs = ListField(Song)


class User(Document):
    userName = StringField(unique=True, required=True, max_length=20, min_length=2)
    playlists = ListField(Playlist)


