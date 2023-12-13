from flask import Blueprint, render_template, request, redirect, url_for
from website.database import UserDB
from website.session import get_session, get_role

rooms = Blueprint('rooms', __name__)


@rooms.route('/rooms', methods=['GET', 'POST'])
def rooms_list():
    if request.method == 'POST':
        room = UserDB.query('SELECT name_type FROM room_type')
        print(room)
        for room_name in room:
            if request.form.get('sub_button') == room_name[0]:
                print(request.form.get('sub_button') + ' ' + room_name[0])
                return redirect(url_for('rooms.rooms_details', room_name=room_name[0]))

    room = UserDB.query('SELECT CONVERT(id_type, CHAR), name_type, price, description FROM room_type')
    return render_template('room/rooms.html', room=room, val_session=get_session(), role=get_role())


@rooms.route('/rooms-details/<room_name>', methods=['GET', 'POST'])
def rooms_details(room_name):
    if room_name:
        room = UserDB.query('SELECT CONVERT(id_type, CHAR), name_type, price, description FROM room_type WHERE name_type=%s', [room_name])
        print(room)
        return render_template('room/rooms-detail.html', _room_=room[0], val_session=get_session(), role=get_role())
