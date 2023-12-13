import os
from website.files import upload_file

from flask import Blueprint, render_template, request, redirect
from website.database import UserDB
from website.session import get_session, get_role, logged_in

management = Blueprint('management', __name__)


@management.route('/manage-room', methods=['GET', 'POST'])
# @logged_in(['staff', 'admin'])
def manage_room():
    if request.method == 'POST':
        room_name = request.form.get('room-name')
        room_description = request.form.get('room-description')
        room_price = request.form.get('room-price')
        UserDB.call_procedure('add_room', (room_name, room_description, room_price))
        id_type = UserDB.query('SELECT id_type FROM room_type WHERE name_type=%s', [room_name])
        id_type = id_type[0][0]
        upload_file(request.files.getlist('room-img'), 'website/static/img/img-room/id-', id_type)

    room = UserDB.query('SELECT * FROM room_type')
    return render_template('manage-room.html', val_session=get_session(), room=room, role=get_role())

