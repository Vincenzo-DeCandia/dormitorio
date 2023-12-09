from flask import Blueprint, render_template, session
from website.session import get_session, get_role

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('index.html', val_session=get_session(), role=get_role())




