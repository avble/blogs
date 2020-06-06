import functools

from flask import render_template
from flask import Blueprint
from flask import request
from flask import session
from flask import flash
from flask import redirect
from flask import url_for
from flask import g


from .db import db_get

bp = Blueprint("auth", __name__)

def login_required(view):
    ''' Decorator  

    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.auth_login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = None
    
    if 'user_id' in session.keys():
        user_id = session['user_id']

    if user_id is None:
        g.user = None
    else:
        g.user = db_get().execute('SELECT * FROM user WHERE username = "%s"' % (user_id)).fetchone()

@bp.route("/auth/login", methods = ('GET', 'POST'))
def auth_login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        db  = db_get()
        account = db.execute(
        'SELECT * FROM user WHERE username = "%s" and password = "%s"' % (username, password)
        ).fetchone()

        if account:
            session.clear()
            session["user_id"] = account["username"]
            #print ('-------%s----------------------', session["user_id"])
            return redirect(url_for("accesscontrol.index"))
        else:
            #print ('-------2----------------------')
            flash("Login Error")

    return render_template('auth/login.html')

@bp.route("/auth/logout", methods = ('GET', 'POST'))
def auth_logout():
    session.clear()
    return redirect(url_for("accesscontrol.index"))
    #return render_template('auth/login.html')
