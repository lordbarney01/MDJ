from celery import Task
from app.entities.managers import SongManager


class TaskAddSong(Task):
    def run(self, youtubeUrl, songName):
        if SongManager.does_entity_with_keys_exist(youtubeUrl=youtubeUrl):
            raise RuntimeError('song already exists')
        return SongManager.create_entity(youtubeUrl=youtubeUrl, songName=songName)

class TaskDeleteSong(Task):
    def run(self, youtubeUrl):
        if not SongManager.does_entity_with_keys_exist(youtubeUrl=youtubeUrl):
            raise RuntimeError('song does not exists')
        return SongManager.delete_song(youtubeUrl=youtubeUrl)
