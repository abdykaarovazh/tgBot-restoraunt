from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from project.config import config

app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.db.db_name}.db'

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'cringe'

app.config['SERVER_NAME'] = f'{config.flask.flask_host}:{config.flask.flask_port}'
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = 'https'

db.init_app(app)
