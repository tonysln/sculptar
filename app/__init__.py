from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_babel import Babel
# from flask_babel import lazy_gettext as _l
from flask import request
import logging
from logging.handlers import RotatingFileHandler
import os


def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Language support
# babel = Babel(app, locale_selector=get_locale)

# DB and alembic
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login and sessions
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Palun logi sisse, et seda lehekülge näha.'

# Logging
if not app.debug:
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/runtime.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Georgi Slavin homepage initialized')


from app import routes, models, errors