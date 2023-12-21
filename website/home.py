from flask import Blueprint, render_template, request
from website.session import get_session, get_role

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('index.html', val_session=get_session(), role=get_role())


@home.route('/contacts')
def contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

    return render_template('contacts.html', val_session=get_session(), role=get_role())




