from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from flask_admin.contrib.peewee import tools
import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tz'

column_default_sort = [['Date', False], ['Time', False]]
admin = Admin(app, name='HydroPi', template_mode='bootstrap3', url='/')
admin.add_view(ModelView(main.PulseData))
# Add administrative views here