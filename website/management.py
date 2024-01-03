from website.files import upload_file

from flask import Blueprint, render_template, request, flash
from website.database import UserDB
from website.session import get_session, get_role, logged_in, user_id

management = Blueprint('management', __name__)


@management.route('/manage-room')
@logged_in(['reception', 'admin'])
def manage_room():
    return render_template('manage/manage-room.html', val_session=get_session(), role=get_role())


@management.route('/manage-room/number', methods=['POST', 'GET'])
@logged_in(['reception', 'admin'])
def manage_room_number():
    if request.method == 'POST' and request.form.get('room-name'):
        room_number = request.form.getlist('room-number[]')
        room_name = request.form.get('room-name')
        id_room = UserDB.query('SELECT id_type FROM room_type WHERE name_type = %s', [room_name])
        for number in room_number:
            UserDB.query('INSERT INTO room (room_number, id_type) VALUES (%s,%s)', (number, id_room[0][0]))
    elif request.method == 'POST' and request.form.get('mod-room-name'):
        room_name = request.form.get('mod-room-name')
        room_number = request.form.get('mod-room-number')
        UserDB.call_procedure('update_room', (room_name, room_number))
    elif request.form.get('deleteRoom'):
        room_number = str(request.form.get('deleteRoom'))
        UserDB.query('DELETE FROM room WHERE room_number=%s', [room_number])
    rooms = UserDB.query('SELECT r1.room_number, r2.name_type FROM room r1 JOIN room_type r2 on r2.id_type = r1.id_type order by r1.room_number');
    return render_template('manage/manage-room-number.html', val_session=get_session(), role=get_role(), room=rooms)


@management.route('/manage-room/type', methods=['GET', 'POST'])
@logged_in(['reception', 'admin'])
def manage_room_type():
    if request.method == 'POST' and request.form.get('save-room') == 'insert':
        room_name = request.form.get('room-name')
        room_description = request.form.get('room-description')
        room_price = request.form.get('room-price')
        optionAdults = request.form.get('optionAdults')
        UserDB.call_procedure('add_type_room', (room_name, room_description, room_price, optionAdults))
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
        print(cleaned_room)
        id_staff = user_id()
        UserDB.call_procedure('add_clean_room', (id_staff, cleaned_room))
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


@management.route('/create-user', methods=['GET', 'POST'])
@logged_in(['admin'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('passw')
        role = request.form.get('role')
        gender = request.form.get('genderOption')
        fiscalCode = request.form.get('fiscalCode')
        phone = request.form.get('phone')
        confirmPassword = request.form.get('confirmPassw')
        if password != confirmPassword:
            flash('Password and Confirm Password must be the same', 'alert-danger')
        else:
            UserDB.call_procedure('create_staff', (fiscalCode, password, name, surname, email, gender, role, phone))
            flash('User successfully created', 'alert-success')
    return render_template('manage/create-user.html', val_session=get_session(), role=get_role())
