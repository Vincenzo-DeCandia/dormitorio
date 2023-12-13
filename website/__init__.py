from flask import Flask, session
import secrets
from datetime import timedelta
from flask_session import Session
from website.session import delete_session, get_session, get_perm_session
from flask_socketio import SocketIO


def create_app():
    app = Flask(__name__)
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
    app.config['SESSION_FILE_THRESHOLD'] = 100000000000
    Session(app)
    socketio = SocketIO(app, cors_allowed_origins="*")

    from .home import home
    from .auth import auth
    from .rooms import rooms
    from .profile import profile
    from .management import management

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(rooms)
    app.register_blueprint(profile)
    app.register_blueprint(management)

    @socketio.on('disconnect')
    def disconnect_user():
        if not get_session() or (get_session() and not get_perm_session()):
            delete_session()
            print('DISCONNECT')

    @socketio.on('connect')
    def connect():
        print('CONNECT')

    return app
