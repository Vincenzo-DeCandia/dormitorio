from flask import session, redirect
from functools import wraps
import os
import base64


def set_session(user_id, role, remember):
    session_id = base64.b64encode(os.urandom(32)).decode('utf-8')
    session.update({'session_id': session_id, 'user_id': user_id, 'role': role})
    if remember:
        session.permanent = True
    else:
        session.permanent = False


def get_session():
    if 'user_id' in session and 'role' in session and 'session_id' in session:
        return True
    else:
        return False


def delete_session():
    session.clear()


def get_perm_session():
    return session.permanent


def get_role():
    return session.get('role')


def user_id():
    return int(session.get('user_id'))


def logged_in(arg_list):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if get_session() and get_role() in arg_list:
                return f(*args, **kwargs)
            else:
                return redirect('404')
        return wrapper
    return decorator

