from flask import Blueprint, render_template_string, render_template, abort, redirect, flash, session
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Email
import uuid
from string import Template

import database

off = Blueprint('offer', __name__,
                        template_folder='templates')

@off.route('/offer/<car>')
def offert(car):
    db = database.Database()
    logged = False
    if 'key' in session:
        if(db.checkSessionID(session['key'])):
            # return redirect('/')
            logged = True
    else:
        session['key'] = "0" # setting session data

    offers,columns = db.getOffert(str(car))

    f = open("./templates/offert.html", "r")
    offert = Template(f.read())
    
    # print(offers)
    offert = offert.substitute(
        Offert_desc=offers[0][3], 
        Offert_img=offers[0][2], 
        Offert_title=offers[0][1],
        Offert_price=offers[0][4],
        Offert_owner=offers[0][5])
    # print(offert)
    return render_template_string(offert, logged = logged)
