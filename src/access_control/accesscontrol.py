import os, sys 
import string
import random
import hashlib

from time import gmtime, strftime
from random import random

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint

from .db import db_get
from .auth import login_required

bp = Blueprint("accesscontrol", __name__)

################################################
### Utility
################################################
def key_generate(user):
    time_now = strftime(user + "%a, %d %b %Y %H:%M:%S +0000", gmtime())
    time_now = "%s-%f" % (time_now, random())
    md = hashlib.md5(time_now.encode())
    md_digest = md.hexdigest()
    return md_digest[-6:]

################################################
##### accesscontrol service #################
@bp.route('/accesscontrol/register', methods = ['POST'])
def accesscontrol_register():
    #print ("Register >> accesscontrol_register >>>ENTER ")
    db = db_get()
    code = key_generate('user')
    shareinfo = request.data.decode('utf-8')
    db.execute(
        "INSERT INTO accesscontrol (code, shareinfo) VALUES (?, ?)",
        (code, shareinfo),
    )
    db.commit()

    return code, 200

@bp.route('/accesscontrol/get/<string:accesscontrol_id>', methods = ['GET'])
def accesscontrol_get(accesscontrol_id):
    db = db_get()
    share_info = db.execute(
        'SELECT shareinfo FROM accesscontrol WHERE code = "%s"' % (accesscontrol_id)
        ).fetchone()

    if share_info:
        return share_info['shareinfo'], 200
    else:
        return "NONE", 200
        

################################################
### view page 
@bp.route('/')
@login_required
def index():
    db = db_get()
    accesscontrols = db.execute(
        "SELECT code, shareinfo, created"
        " FROM accesscontrol"
        " ORDER BY created DESC"
    ).fetchall()

    return render_template('accesscontrol/index.html', accesscontrols=accesscontrols)

@bp.route('/accesscontrol/delete/<string:accesscontrol_id>', methods = ('POST', 'GET'))
def accesscontrol_delete(accesscontrol_id):
    # Get formdate
    db = db_get()
    sql_string =  "DELETE FROM accesscontrol WHERE code = \"%s\"" % (accesscontrol_id)
    #print ( "accesscontrol_delete >>> " + sql_string + " accesscontrol_delete >>>")
    db.execute(sql_string)
    db.commit()

    return redirect(url_for("accesscontrol.index"))
