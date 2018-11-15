from flask import Flask
from app.api.config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from celery import Celery

login = LoginManager()
login.login_view = 'gui-routes.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db = MongoEngine()

    db.init_app(app)
    login.init_app(app)
    from app.api.routes import app as routes
    from app.api.songs import app as api_bp
    app.debug = True
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(routes, url_prefix='/')
    celery = Celery(app.name, broker=Config.BROKER)
    celery.conf.update(app.config)
    return app


if __name__ == "__main__":

    app = create_app()
    app.run()
