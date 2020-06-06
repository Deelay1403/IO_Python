from flask import Flask, render_template,flash, redirect
from string import Template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_socketio import SocketIO, emit

class GUI:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'you-will-never-guess'
        self.socketio = SocketIO(self.app)

    def run(self):
        self.app.run()