from flask import Blueprint, render_template, redirect, request
import requests
from website.database import UserDB, AdminDB
from website.session import *

# Define a new blueprint for authentication route
auth = Blueprint('auth', __name__)


# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Initialize a message variable
    msg = None

    if get_session():
        return redirect('/')

    # If request method is POST and the user is not logged in get the data from the form
    if request.method == 'POST' and not get_session():

        fiscal_code = request.form.get('cod_fisc')
        password = request.form.get('password')
        remember = request.form.get('remember')

        staff = UserDB.call_procedure('check_staff', (fiscal_code, password, 0))
        print(staff)
        if staff:
            staff_exist = staff[2]
            if staff_exist:
                staff_info = AdminDB.query('SELECT id_staff, role FROM staff WHERE s_fiscal_code=%s', [fiscal_code])

                set_session(staff_info[0][0], staff_info[0][1], remember)
                return redirect('/')

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
                response = requests.get('https://api.uniparthenope.it/UniparthenopeApp/v1/login', auth=(fiscal_code, password))

                # If GET request return 200, store user into database and then redirect to homepage
                if response.status_code == 200:

                    res = response.json()
                    matr = res['user']['trattiCarriera'][0]['matricola']
                    name = res['user']['firstName']
                    surname = res['user']['lastName']
                    gender = res['user']['sex']
                    role = 'user'

                    # Method register_user calls a stored procedure which register a record into the database
                    success_create = UserDB.call_procedure('create_user', (matr, None, fiscal_code, password, name, surname, gender, role))
                    if success_create is None:
                        return render_template('login.html', msg='Errore durante la creazione', val_session=get_session())
                    else:
                        user_id = UserDB.query('SELECT id FROM user WHERE fiscal_code=%s', [fiscal_code])
                        set_session(user_id, role, remember)
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

