from flask import abort, render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateEntryForm
from app.models import User, Monument, Photo
# from flask_babel import _
from math import ceil
import random
import os
import uuid
import json
from .services import UserService


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Kodu')


@app.route('/monuments')
def monuments():
    return render_template('monuments.html', title='Skulptuurid')


@app.route('/create')
@login_required
def create():
    form = CreateEntryForm()
    if form.validate_on_submit():
        pass

    return render_template('create.html', title='Lisa uus skulptuur', form=form)


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Konto')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', title='Admin')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Olete välja logitud')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exists
        user = UserService.get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data): # verify password
            flash('Vale kasutajanimi või parool')
            return redirect(url_for('login'))

        app.logger.info('Logging in user %s', user.username)
        UserService.log_user_in(user, form.remember_me.data)

        # Redirect to original page, or index
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Logi sisse', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        d = {'username': form.username.data, 
            'email': form.email.data,
            'full_name': form.full_name.data,
            'password': form.password.data
        }
        UserService.post_user(d)
        flash('Kasutaja loomine õnnestus!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Registreeru', form=form)
