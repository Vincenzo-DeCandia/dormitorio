from flask import Blueprint, render_template, session, redirect, request
import requests
from website.db import UserDB

# Define a new blueprint for authentication route
auth = Blueprint('auth', __name__)


# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Initialize a message variable
    msg = None

    # If user is logged in redirect to homepage
    if session.get('username'):
        return redirect('/')

    # If request method is POST and the user is not logged in get the data from the form
    if request.method == 'POST' and not session.get('username'):
        username = request.form.get('cod_fisc')
        password = request.form.get('password')

        # Check the student into the database
        student = UserDB.check_user(username, password)

        # If the student exist, set session variable and redirect to homepage
        if student:
            session['username'] = username
            return redirect('/')
        else:
            # If student doesn't exist, check credentials with UniParthenope API
            response = requests.get('https://api.uniparthenope.it/UniparthenopeApp/v1/login', auth=(username, password))

            # If GET request return 200, store user into database and then redirect to homepage
            if response.status_code == 200:

                session['username'] = username

                res = response.json()
                matr = res['user']['trattiCarriera'][0]['matricola']
                name = res['user']['firstName']
                surname = res['user']['lastName']
                gender = res['user']['sex']
                role = res['user']['grpDes']

                # Method register_user calls a stored procedure which register a record into the database
                UserDB.register_user(matr, username, password, name, surname, gender, role)
                return redirect('/')

            else:
                # After insert wrong credentials it will print an error message
                msg = 'Invalid credentials'
                return render_template('login.html', msg=msg, val_session=False)

    elif session.get('username'):
        return redirect('/')

    return render_template('login.html', msg=msg, val_session=False)


# Route for logout
@auth.route('/logout')
def logout():
    # Remove username from session and redirect to login page
    session.pop('username', None)
    return redirect('/login')
