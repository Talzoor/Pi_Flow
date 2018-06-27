from flask import Flask
from flask_admin import Admin


app = Flask(__name__)

admin = Admin(app, name='HydroPi', template_mode='bootstrap3')
# Add administrative views here

@app.route('/')
def index():
    return 'Nice....'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')