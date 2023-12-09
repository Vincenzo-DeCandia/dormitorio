from flask import session, redirect
from functools import wraps
import os
import base64


def set_session(user_id, role, remember):
    session['session_id'] = base64.b64encode(os.urandom(32)).decode('utf-8')
    session['user_id'] = user_id
    session['role'] = role
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
    return session.get('user_id')


def logged_as_cleaner(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if get_session() and get_role() == 'cleaner':
            return f(*args, **kwargs)
        else:
            return redirect('/forbidden')
    return decorated_func


def logged_as_reception(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if get_session() and get_role() == 'reception':
            return f(*args, **kwargs)
        else:
            return redirect('/forbidden')
    return decorated_func


def logged_as_admin(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if get_session() and get_role() == 'admin':
            return f(*args, **kwargs)
        else:
            return redirect('/forbidden')
    return decorated_func


def logged_as_user(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if get_session() and get_role() == 'user':
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return decorated_func
