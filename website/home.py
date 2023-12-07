from flask import Blueprint, render_template
from website.session import *

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('index.html', val_session=get_session(), role=get_role())




