from flask import Blueprint, render_template, request, redirect, url_for
from website.session import get_session, get_role
from website.database import UserDB

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        checkIn = request.form.get('checkin')
        checkOut = request.form.get('checkout')
        adults = request.form.get('adults')
        return redirect(url_for('home.search_room', check_in=checkIn, check_out=checkOut, adults=adults))
    return render_template('index.html', val_session=get_session(), role=get_role())


@home.route('/contacts')
def contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

    return render_template('contacts.html', val_session=get_session(), role=get_role())


@home.route('/search/<check_in>+<check_out>+<adults>', methods=['GET', 'POST'])
def search_room(check_in, check_out, adults):
    rooms = UserDB.query('SELECT CONVERT(t2.id_type, CHAR), CONCAT(UCASE(LEFT(t2.name_type, 1)), SUBSTRING(t2.name_type, 2)), t1.available FROM (SELECT t1.id_type, (total_room - busy_room) as available FROM (SELECT id_type, count(*) AS busy_room FROM reservation WHERE (check_in_date <= %s and check_out_date >= %s and end_date is null) or (check_in_date <= %s and end_date >= %s) GROUP BY id_type) t1 JOIN (SELECT id_type, count(*) AS total_room FROM room GROUP BY id_type) t2 ON t1.id_type = t2.id_type) t1 JOIN room_type t2 on t1.id_type=t2.id_type WHERE t2.adults = %s', (check_in, check_out, check_in, check_out, adults))
    return render_template('room/search-room.html', val_session=get_session(), role=get_role(), rooms=rooms)






