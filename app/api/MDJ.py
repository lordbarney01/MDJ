from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from celery import Celery


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login.init_app(app)
    from app.routes import bp as routes
    from app.api import bp as api_bp
    app.debug = True
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(routes, url_prefix='/')
    celery = Celery(app.name, broker='amqp://MDJ:asdasd@localhost:5672/MDj_host')
    celery.conf.update(app.config)
    return app


if __name__ == "__main__":
    db = MongoEngine()
    login = LoginManager()
    login.login_view = 'login'
    app = create_app()
    app.run()
