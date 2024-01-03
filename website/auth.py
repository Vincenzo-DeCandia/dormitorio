from flask import Blueprint, render_template, request, url_for
import requests
from website.database import UserDB, AdminDB
from website.session import *
import pyotp
from io import BytesIO
import qrcode
from base64 import b64encode
import shutil

# Define a new blueprint for authentication route
auth = Blueprint('auth', __name__)


def get_b64encoded_qr_image(data):
    print(data)
    qr = qrcode.main.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered)
    return b64encode(buffered.getvalue()).decode("utf-8")


@auth.route('/verify2FA/<fiscal_code>&remember=<remember>', methods=['GET', 'POST'])
def verify2fa(fiscal_code, remember):
    _2fa = UserDB.query('SELECT secret_key FROM staff WHERE s_fiscal_code = %s', [fiscal_code])
    secret_key = _2fa[0][0]
    totp = pyotp.totp.TOTP(secret_key)
    if request.method == "POST":
        otp = request.form.get('otp')
        print(totp.now())
        if totp.now() == otp:
            staff = UserDB.query('SELECT id_staff, role FROM staff WHERE s_fiscal_code = %s', [fiscal_code])
            set_session(staff[0][0], staff[0][1], remember)
            return redirect('/')
        else:
            return redirect(url_for('auth.verify2fa', fiscal_code=fiscal_code, remember=remember))
    return render_template('verify2fa.html', fiscal_code=fiscal_code, remember=remember)


@auth.route('/setup2FA/<fiscal_code>&remember=<remember>', methods=['GET', 'POST'])
def setup2fa(fiscal_code, remember):
    _2fa = UserDB.query('SELECT secret_key, access FROM staff WHERE s_fiscal_code = %s', [fiscal_code])
    secret_key = _2fa[0][0]
    uri = pyotp.totp.TOTP(secret_key[0][0]).provisioning_uri(name=fiscal_code)
    if request.method == "POST":
        return redirect(url_for('auth.verify2fa', uri=uri, fiscal_code=fiscal_code, remember=remember))
    base64_qr_image = get_b64encoded_qr_image(uri)
    return render_template('setup2fa.html', uri=uri, qr_image=base64_qr_image, fiscal_code=fiscal_code,
                           remember=remember, secret=secret_key)


# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Initialize a message variable
    msg = None

    if get_session():
        return redirect('/')

    # If request method is POST and the user is not logged in get the data from the form
    if request.method == 'POST' and not get_session():
        print('POST LOGIN')
        fiscal_code = request.form.get('cod_fisc')
        password = request.form.get('password')
        remember = request.form.get('remember')
        if remember:
            remember = True
        else:
            remember = False

        staff = UserDB.call_procedure('check_staff', (fiscal_code, password, 0))
        print(staff)
        if staff:
            staff_exist = staff[2]

            if staff_exist:
                _2fa = UserDB.query('SELECT access FROM staff WHERE s_fiscal_code = %s', [fiscal_code])
                access = _2fa[0][0]
                if access:
                    return redirect(url_for('auth.verify2fa', fiscal_code=fiscal_code, remember=remember))
                else:
                    return redirect(url_for('auth.setup2fa', fiscal_code=fiscal_code, remember=remember))

        # Check the student into the database
        user = UserDB.call_procedure('check_user', (fiscal_code, password, 0))
        print(user)

        # If the student exist, set session variable and redirect to homepage
        if user:
            user_exist = user[2]
            if user_exist:
                info = UserDB.query('SELECT id_user, role FROM user WHERE fiscal_code=%s', [fiscal_code])
                print(info)
                set_session(info[0][0], info[0][1], remember)
                return redirect('/')
            else:
                # If student doesn't exist, check credentials with UniParthenope API
                response = requests.get('https://api.uniparthenope.it/UniparthenopeApp/v1/login',
                                        auth=(fiscal_code, password))
                print(True)
                # If GET request return 200, store user into database and then redirect to homepage
                if response.status_code == 200:

                    res = response.json()
                    matr = res['user']['trattiCarriera'][0]['matricola']
                    name = res['user']['firstName']
                    surname = res['user']['lastName']
                    gender = res['user']['sex']
                    role = 'user'

                    # Method register_user calls a stored procedure which register a record into the database
                    success_create = UserDB.call_procedure('create_user', (
                        matr, None, fiscal_code, password, name, surname, gender, role))
                    if success_create is None:
                        return render_template('login.html', msg='Errore durante la creazione', val_session=get_session())
                    else:
                        user_id = UserDB.query('SELECT id_user FROM user WHERE fiscal_code=%s', [fiscal_code])[0][0]
                        set_session(user_id, role, remember)
                        user_id = str(user_id)
                        os.mkdir('website/static/img/avatar/id-' + user_id)
                        shutil.copy('website/static/img/avatar/default.webp', 'website/static/img/avatar/id-' + user_id + '/default.webp')
                        UserDB.query('INSERT INTO avatar_user (name_avatar, id_user) VALUES (%s, %s)', ('default.webp', user_id))
                        return redirect('/')

                else:
                    # After insert wrong credentials it will print an error message
                    msg = 'Invalid credentials'
                    return render_template('login.html', msg=msg, val_session=get_session())

    return render_template('login.html', msg=msg, val_session=get_session())


# Route for logout
@auth.route('/logout')
def logout():
    delete_session()
    return redirect('/login')
