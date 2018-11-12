from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes
from app.api import bp as api_bp
app.debug = True
app.register_blueprint(api_bp, url_prefix='/api')

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

