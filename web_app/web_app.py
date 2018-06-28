from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tz'

admin = Admin(app, name='HydroPi', template_mode='bootstrap3', url='/')
admin.add_view(ModelView(main.Pulse_data))
# Add administrative views here