from flask import Flask
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHMEY_TRACK_NOTIFICATIONS'] = False
app.config['SECRET_KEY'] = 'testing for the cows'