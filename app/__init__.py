from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager


db = MongoEngine()
login = LoginManager()
login.login_view = 'login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login.init_app(app)
    from app.routes import bp as routes
    from app.api import bp as api_bp
    app.debug = True
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(routes, url_prefix='/')

    return app

#from app.models import Song
#song = Song()
#song.youtubeUrl = "https://www.youtube.com/watch?v=sKZN115n6MI"
#song.songName = "Everything in its right place"
#song.author = "Radiohead"
#song.genre = [
#       "Alternative",
#       "Rock",
#       "2000",
#       "Exprimental"
#   ]
#song.save()

