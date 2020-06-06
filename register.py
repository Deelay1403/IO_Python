from flask import Blueprint, render_template, abort, redirect, session
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Email
import database
from user import User

class RegisterForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(),Email()])
    submit = SubmitField('Sign Up')

reg = Blueprint('register', __name__,
                        template_folder='templates')
    
@reg.route('/signup', methods=['GET', 'POST'])
def signup():
    db = database.Database()
    if 'key' in session:
        if(db.checkSessionID(session['key'])):
            return redirect('/')
    else:
        session['key'] = "" # setting session data

    error = None
    form = RegisterForm()
    if(form.validate_on_submit()):
        user = User(
            form.username.data,
            form.password.data,
            form.email.data)
        if(not db.addUser(user)):
            return redirect("/signin")
        else:
            error = "User already exist"
    try:
        return render_template('signup.html',title='Sign Up',form=form, error=error)
    except TemplateNotFound:
        abort(404)
    