from flask import Blueprint, render_template_string, render_template, abort, redirect, flash, session
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Email
import uuid
from string import Template
import questionnaire
import database

class QuestionnaireForm(FlaskForm):
    made = StringField('Made', validators=[DataRequired()])
    year_min = StringField('Min', validators=[DataRequired()])
    year_max = StringField('Max', validators=[DataRequired()])
    price_min = StringField('Min', validators=[DataRequired()])
    price_max = StringField('Max', validators=[DataRequired()])
    submit = SubmitField('Sign Query')

class deleteQuest(FlaskForm):
    cancerQuest = SubmitField('Delete Questionnaire')

class Password(FlaskForm):
    oldPass = PasswordField('Stare hasło', validators=[DataRequired()])
    newPass = PasswordField('Nowe hasło', validators=[DataRequired()])
    submit = SubmitField('Sign In')
con = Blueprint('control', __name__,
                        template_folder='templates')

@con.route('/control', methods=['GET', 'POST'])
def control():
    db = database.Database()
    logged = False
    error = ""
    info = ""
    if 'key' in session:
        if(db.checkSessionID(session['key'])):
            # return redirect('/')
            logged = True
    else:
        session['key'] = "0" # setting session data
        return redirect('/signin')
    
    # OffertList
    (result,names) = db.getOffertNamesByUsername(session['username'])
    offerList = ""
    for i in range(len(result)):
        offerList += F"<a class='offert-link' href='/offer/{result[i][0]}'> <li class='offert'>{result[i][1]}</li></a>\n"
    questionnaireFilled = db.checkQuest(session['username'])
    quest = QuestionnaireForm()
    password = Password()
    deletequest = deleteQuest()

    if quest.is_submitted() and quest.submit.data and str(quest.made.data)!="":
        q = questionnaire.Questionnaire(
            session['username'],
            quest.made.data,
            quest.year_min.data,
            quest.year_max.data,
            quest.price_min.data,
            quest.price_max.data
        )
        if(not db.sendQuestionnaire(q)):
            return redirect("/control")
    elif deletequest.is_submitted() and deletequest.cancerQuest.data:
        if(not db.deleteQuestionnaire(session['username'])):
            return redirect("/control")
    elif password.is_submitted() and password.newPass.data!="":
        if(not db.changePass(session['username'], 
        password.oldPass.data, 
        password.newPass.data)):
            info = "Password has changed"
            return redirect("/control")
        else:
            error = "Wrong old password"

    return render_template('control.html',
    offerList = offerList,
    questionnaireFilled = questionnaireFilled, 
    questionnaire=quest,
    password = password,
    deletequest = deletequest,
    info = info,
    error = error,
    logged = logged)
