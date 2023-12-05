from flask import Flask
from datetime import timedelta
from flask_session import Session


def create_app():
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY'] = 'secret__key'
    app.permanent_session_lifetime = timedelta(minutes=30)
    Session(app)

    from .home import home
    from .auth import auth
    from .rooms import rooms

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(rooms)

    return app
