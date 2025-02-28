from flask import Blueprint, render_template_string, render_template, abort, redirect, flash, session
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired,Email
import uuid

import database
from offerTemplate import OfferTemplate

class OffertForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    model = StringField('model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    make = StringField('Name', validators=[DataRequired()])
    photo = StringField('Photo', validators=[DataRequired()])
    typ = SelectField('Type',choices=[('Elektryczny','Elektryczny')
    ,('Hybryda','Hybryda')
    ,('Wodorowe','Wodorowe')])
    desc = StringField('Desc', widget=TextArea(),validators=[DataRequired()])
    submit = SubmitField('Dodaj')

offer = Blueprint('makeoffert', __name__,
                        template_folder='templates')

@offer.route('/makeoffert', methods=['GET', 'POST'])
def makeoffert():
    db = database.Database()
    logged = False
    if 'key' in session:
        if(db.checkSessionID(session['key'])):
            logged = True
    else:
        session['key'] = "0" # setting session data
        return redirect("/signin")
        
    error = None
    offer = OffertForm()
    if offer.validate_on_submit():
        o = OfferTemplate(
            session['username'],
            offer.name.data,
            offer.model.data,
            offer.price.data,
            offer.make.data,
            offer.year.data,
            offer.photo.data,
            offer.typ.data,
            offer.desc.data
        )
        if(not db.AddOffert(o)):
            return redirect('/')

    return render_template('makeoffert.html',
    offer=offer,
    logged=logged)