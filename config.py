import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGODB_SETTINGS = {
        'db': 'DJ_DB',
        'host': '127.0.0.1',
    }
    #
    #}
