from flask import Blueprint,Flask, render_template,flash, redirect, session, render_template_string
from string import Template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import database
import GUI
from register import reg
from login import log
from offert import off
from control import con
from makeoffert import offer
gui = GUI.GUI()

@gui.socketio.on('disconnect')
def disconnect_user():
    if(not session['remember']):
        session.pop('key', "0")

@gui.app.route("/")
def main():
    db = database.Database()
    logged = False
    if 'key' in session:
        if(db.checkSessionID(session['key'])):
            # return redirect('/')
            logged = True
    else:
        session['key'] = "0" # setting session data
    
    # db.addCar("A4","Audi","Elektryczny")
    offers,columns = db.getOffers_index()
    f = open("./templates/index.html", "r")
    index = Template(f.read())

    f = open("./templates/container.html", "r")
    container = f.read()
    f.close()

    container_id = open("./static/containter_id.css", "r")
    con_id = container_id.read()
    container_id.close()

    containers = ""
    container_id_css = ""
    for i in range(len(offers)):
        cont_id = Template(con_id)
        cont_id = cont_id.substitute(CSS_id=offers[i][0],CSS_image=offers[i][2])
        container_id_css+= cont_id + "\n\n"
        # print(container_id_css)
        cont = Template(container)
        # print(str(cont_id))
        cont = cont.substitute(CSS_id = offers[i][0],Car_name=offers[i][1])
        containers += cont + "\n"
    index = index.substitute(container = containers, car_id_css=str(container_id_css))
    return render_template_string(index, logged = logged)

if __name__ == "__main__":
    gui.app.register_blueprint(reg)
    gui.app.register_blueprint(log)
    gui.app.register_blueprint(off)
    gui.app.register_blueprint(con)
    gui.app.register_blueprint(offer)
    gui.run()
    