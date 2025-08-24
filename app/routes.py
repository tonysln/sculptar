from flask import abort, render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm#, UploadForm, EditForm
from app.models import User, Monument, Photo
from werkzeug.utils import secure_filename
# from flask_babel import _
from PIL import Image
from math import ceil
from datetime import datetime
import random
import os
import uuid
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/monuments')
def monuments():
    return render_template('monuments.html', title='Monuments')


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', title='Admin')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exists
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))

        if user is None or not user.check_password(form.password.data): # verify password
            flash('Invalid username or password')
            return redirect(url_for('login'))

        app.logger.info('Logging in user %s', user.username)
        login_user(user, remember=form.remember_me.data)

        user.last_login = datetime.now()
        db.session.commit()

        # Redirect to original page, or index
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    email=form.email.data,
                    full_name=form.full_name.data)
        user.set_password(form.password.data)

        app.logger.info('[!] New user registration: %s - %s', user.username, user.full_name, user.email)

        db.session.add(user)
        db.session.commit()

        flash('You are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)
