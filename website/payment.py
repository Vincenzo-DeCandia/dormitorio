from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
import requests
from website.session import *
from website.database import UserDB

payment = Blueprint('payment', __name__)


@payment.route('/checkout/review/cod=<id_room>', methods=['GET', 'POST'])
def payment_view(id_room):
    price = 0.0
    if request.method == 'POST':
        pass
    price = round(UserDB.call_procedure('view_price', (id_room, price))[1], 2)
    name_room = UserDB.query('SELECT name_type FROM room_type WHERE id_type = %s', [id_room])[0][0]
    c_card = UserDB.query('SELECT name, number_card, exp, cvc, type FROM payment_method WHERE id_user = %s', [user_id()])
    return render_template('payment/checkout.html',name_room=name_room, price=price, cards=c_card)

