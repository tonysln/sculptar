from flask import make_response
from app.models import User, Monument, Photo
from flask_login import login_user
from app import app, db
import sqlalchemy as sa
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import os


class Service:
    pass


class UserService(Service):
    @staticmethod
    def get_user_by_username(username):
        """Return user entry with specific given username"""
        user = db.session.scalar(sa.select(User).where(User.username == username))
        return user

    @staticmethod
    def log_user_in(user, remember_me):
        """Calls login_user on given user object and updates last_login timestamp"""
        login_user(user, remember=remember_me)
        user.last_login = datetime.now()
        db.session.commit()
        return True

    @staticmethod
    def post_user(data):
        """Create and save new user entry from given data"""
        user = User(username=data['username'], 
                    email=data['email'],
                    full_name=data['full_name'])
        user.set_password(data['password'])

        app.logger.info('[!] New user registration: %s - %s', user.username, user.full_name, user.email)

        db.session.add(user)
        db.session.commit()
        return True
