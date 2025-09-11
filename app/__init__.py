from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_babel import Babel
# from flask_babel import lazy_gettext as _l
from flask import request
import cloudinary
import logging
import os


def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


# DB and alembic
db = SQLAlchemy()
migrate = Migrate()

# Login and sessions
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Palun logi sisse, et seda lehekülge näha.'

# Language support
# babel = Babel(app, locale_selector=get_locale)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    # babel.init_app(app, locale_selector=get_locale)

    cloudinary.config(
        cloud_name = app.config['CLOUDINARY_NAME'],
        api_key = app.config['CLOUDINARY_API_KEY'],
        api_secret = app.config['CLOUDINARY_API_SECRET'],
        secure = True
    )

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


    # Logging
    if not app.debug and not app.testing:
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
            app.logger.info('SCULPTURA TARBATUM initialized')

    return app


from app import models
