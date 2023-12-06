import mysql.connector
from flask import Blueprint, render_template, session, redirect, request
import requests
from website.database import UserDB

# Define a new blueprint for authentication route
auth = Blueprint('auth', __name__)


# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Initialize a message variable
    msg = None

    # If request method is POST and the user is not logged in get the data from the form
    if request.method == 'POST' and not session.get('fiscal_code'):
        fiscal_code = request.form.get('cod_fisc')
        password = request.form.get('password')

        # Check the student into the database
        user = UserDB.call_procedure('check_user', (fiscal_code, password, 0))
        user_exist = user[2]

        # If the student exist, set session variable and redirect to homepage
        if user is None:
            print('Error during the fetch')
            msg = 'Error during the fetch'
        elif user_exist:
            session['fiscal_code'] = fiscal_code
            code = UserDB.query('SELECT role FROM user WHERE fiscal_code=%s', [fiscal_code])
            session['role'] = code[0][0]
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
                role = res['user']['grpDes']

                # Method register_user calls a stored procedure which register a record into the database
                success_create = UserDB.call_procedure('create_user', (matr, None, fiscal_code, password, name, surname, gender, role))
                if success_create is None:
                    return render_template('login.html', msg='Errore durante la creazione', val_session=False)
                else:
                    session['fiscal_code'] = fiscal_code
                    session['role'] = role
                    return redirect('/')

            else:
                # After insert wrong credentials it will print an error message
                msg = 'Invalid credentials'
                return render_template('login.html', msg=msg, val_session=False)

    elif session.get('fiscal_code'):
        return redirect('/')

    return render_template('login.html', msg=msg, val_session=False)


# Route for logout
@auth.route('/logout')
def logout():
    # Remove username from session and redirect to login page
    session.pop('fiscal_code', None)
    return redirect('/login')


@auth.route('/get')
def get():
    return session.get('fiscal_code') + ' ' + session.get('role')
