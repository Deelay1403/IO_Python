from flask import Blueprint, render_template_string, render_template, abort, redirect, flash, session
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Email
import uuid

import database
from user import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

log = Blueprint('login', __name__,
                        template_folder='templates')

@log.route('/signin', methods=['GET', 'POST'])
def signin():
    db = database.Database()
    logged = False
    if 'key' in session:
        if(db.checkSessionID(session['key'])):
            return redirect('/')
            logged = True
    else:
        session['key'] = "0" # setting session data
        
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        
        user = User(form.username.data,form.password.data)
        if(db.getLoginState(user)):
            session['key'] = uuid.uuid4()
            session['username'] = user.username
            db.setSessionID(session['key'],user.username)
            session['remember'] = form.remember_me.data
            return redirect('/')
        else:
            error = "Wrong credentials"
    return render_template('signin.html', 
    title='Sign In', 
    form=form, 
    error=error, 
    logged = logged)
@log.route('/logout')
def logout():
    session['key'] = "0"
    return redirect('/')