from website.files import upload_file

from flask import Blueprint, render_template, request, redirect, jsonify
from website.database import UserDB
from website.session import get_session, get_role, logged_in, user_id

management = Blueprint('management', __name__)


@management.route('/manage-room')
@logged_in(['reception', 'admin'])
def manage_room():
    return render_template('manage/manage-room.html', val_session=get_session(), role=get_role())


@management.route('/manage-room/number')
@logged_in(['reception', 'admin'])
def manage_room_number():
    pass


@management.route('/manage-room/type', methods=['GET', 'POST'])
@logged_in(['reception', 'admin'])
def manage_room_type():
    if request.method == 'POST' and request.form.get('save-room') == 'insert':
        room_name = request.form.get('room-name')
        room_description = request.form.get('room-description')
        room_price = request.form.get('room-price')
        UserDB.call_procedure('add_room', (room_name, room_description, room_price))
        id_type = UserDB.query('SELECT id_type FROM room_type WHERE name_type=%s', [room_name])
        id_type = id_type[0][0]
        upload_file(request.files.getlist('room-img'), 'website/static/img/img-room/id-', id_type)
    elif request.method == 'POST' and request.form.get('save-room') == 'modify':
        id_room = request.form.get('mod-id-room')
        room_description = request.form.get('mod-room-description')
        room_price = request.form.get('mod-room-price')
        UserDB.query('UPDATE room_type SET description=%s, price=%s WHERE id_type=%s', (room_description, room_price, id_room))
    elif request.form.get('deleteRoom'):
        id_room = request.form.get('deleteRoom')
        UserDB.query('DELETE FROM room_type WHERE id_type=%s', [id_room])

    room = UserDB.query('SELECT * FROM room_type')
    return render_template('manage/manage-room_type.html', val_session=get_session(), room=room, role=get_role())


@management.route('/clean-room', methods=['GET', 'POST'])
@logged_in(['cleaner', 'admin'])
def clean_room():
    if request.method == 'POST':
        cleaned_room = request.form.get('checkRoom')
        id_staff = user_id()
        UserDB.clean_room('add_clean_room', (id_staff, cleaned_room))
    room = UserDB.query('SELECT * FROM view_room_not_cleaned')
    return render_template('manage/clean-room.html', val_session=get_session(), role=get_role(), rooms=room)


@management.route('/manage-promotion', methods=['GET', 'POST'])
@logged_in(['reception', 'admin'])
def manage_promotion():

    if request.method == 'POST' and request.form.get('deletePromotion'):
        id_promotion = request.form.get('deletePromotion')
        UserDB.call_procedure('delete_promotion', [id_promotion])
        print('promotion deleted')
    elif request.method == 'POST':
        id_promotion = request.json['promotion_id']
        name_room = request.json['room_name']
        name_promotion = request.json['promotion_name']
        start_date = request.json['promotion_start']
        end_date = request.json['promotion_end']
        discount = request.json['promotion_discount']
        print(id_promotion, name_room, name_promotion, start_date, end_date, discount)
        if not id_promotion:
            UserDB.call_procedure('add_promotion', (name_promotion, start_date, end_date, discount))
            id_promotion = UserDB.query('SELECT * FROM promotion where promotion_name = %s', [name_promotion])[0][0]
            for room in name_room:
                print(room)
                UserDB.call_procedure('add_promotion_room', (id_promotion, room))
        else:
            UserDB.call_procedure('modify_promotion', (id_promotion, name_promotion, start_date, end_date, discount))
        return {'response': True}

    promotion = UserDB.query('SELECT * FROM view_promotion')
    return render_template('manage/manage-promotion.html', val_session=get_session(), role=get_role(), promotions=promotion)


