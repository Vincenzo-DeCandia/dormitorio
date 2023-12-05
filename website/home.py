from flask import Blueprint, render_template, session

home = Blueprint('home', __name__)


@home.route('/')
def index():
    val_session = False
    external_css_url = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
    if session.get('username'):
        val_session = True
        return render_template('index.html', external_css_url=external_css_url, val_session=val_session)
    return render_template('index.html', external_css_url=external_css_url, val_session=val_session)
