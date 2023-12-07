from flask import Blueprint, render_template

rooms = Blueprint('rooms', __name__)


@rooms.route('/rooms', methods=['GET', 'POST'])
def rooms_list():

    return render_template('rooms.html')

