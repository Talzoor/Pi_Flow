from flask import Flask
from flask_admin import Admin
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from peewee import *
import datetime
# create an Auth object for use with our flask app and database wrapper


DATABASE_NAME = './Readings.db'

app = Flask(__name__)

@app.route('/')
def index():
    return 'NiceLy....'


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')