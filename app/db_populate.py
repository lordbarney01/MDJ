import json
from mongoengine import connect
from app.entities.managers import SongManager, UserManager
from app.config import Config


def main():
    connect(Config.MONGODB_SETTINGS['db'])

    with open('db_config.json') as data_file:
        data = json.load(data_file)

    for song in data["songs"]:
        SongManager.create_item(songName=song['songName'], youtubeUrl=song['youtubeUrl'])

    for user in data["users"]:
        UserManager.create_entity(userName=user["userName"])


if __name__ == '__main__':
    main()
