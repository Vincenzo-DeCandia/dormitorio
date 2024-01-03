import requests
from flask import Blueprint, render_template, request, redirect
from website.session import *
from website.database import UserDB

profile = Blueprint('profile', __name__)


@profile.route('/reception-profile')
@logged_in(['reception', 'admin', 'cleaner'])
def reception_profile():
    return render_template('profile-reception.html', val_session=get_session(), role=get_role())


@profile.route('/profile', methods=['GET', 'POST'])
@logged_in(['user'])
def user_profile():
    if request.method == 'POST':
        avatar = request.files['avatar']
        filename = avatar.filename
        avatar.save(os.path.join('website/static/img/avatar/id-' + str(user_id()), filename))
        UserDB.query('UPDATE avatar_user SET name_avatar=%s WHERE id_user=%s', (avatar.filename, user_id()))
    user = UserDB.query('SELECT matriculation_number, email, fiscal_code, name, surname, gender FROM user WHERE id_user=%s', [user_id()])
    name_avatar = UserDB.query('SELECT name_avatar FROM avatar_user WHERE id_user=%s', [user_id()])
    path_avatar = 'img/avatar/id-' + str(user_id()) + '/' + name_avatar[0][0]
    print(path_avatar)
    return render_template('profile-user.html', val_session=get_session(), role=get_role(), user=user[0], path_avatar=path_avatar)


@profile.route('/mysettings', methods=['GET', 'POST'])
@logged_in(['user'])
def mysettings():
    if request.method == 'POST' and request.form.get('sub_method') == 'Aggiungi':
        cc_name = request.form.get('cc-name')
        cc_number = request.form.get('cc-number')
        cc_exp = request.form.get('cc-exp')
        cc_cvc = request.form.get('cc-cvc')
        cc_type = 'visa'
        UserDB.query('INSERT INTO payment_method (number_card, id_user, exp, name, cvc, type) VALUES (%s, %s, %s, %s, %s, %s)', (cc_number, user_id(), cc_exp, cc_name, cc_cvc, cc_type))
    elif request.form.get('cc-number-del'):
        UserDB.query('DELETE FROM payment_method WHERE number_card = %s', [request.form.get('cc-number-del')])
    card = UserDB.query('SELECT number_card, exp, name, type FROM payment_method WHERE id_user=%s', [user_id()])
    return render_template('settings/settings-user.html', val_session=get_session(), role=get_role(), cards=card)


@profile.route('/history-reservation')
@logged_in(['user'])
def history_reservation():
    reservation = UserDB.query('SELECT r1.id_reservation, r1.reservation_date, r1.check_in_date, r1.check_out_date, rt.name_type, p.total, r1.cancelled FROM reservation r1 left JOIN payment p on r1.id_reservation = p.id_reservation JOIN reservation_user r2 on r1.id_reservation = r2.id_reservation JOIN room_type rt on r1.id_type = rt.id_type WHERE r2.id_user = %s', [user_id()])
    print(reservation)
    return render_template('booking/history-reserv.html', val_session=get_session(), role=get_role(), reservations=reservation)

