from flask import Blueprint, render_template
from website.session import *

profile = Blueprint('profile', __name__)


@profile.route('/reception-profile')
@logged_as_reception
def reception_profile():
    return render_template('profile-reception.html')


@profile.route('/profile')
@logged_as_user
def user_profile():
    return render_template('profile-user.html')
