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
from .services import UserService, MonumentService


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Kodu')


@app.route('/monuments')
def monuments():
    items = MonumentService.get_all_monuments_with_photos()
    return render_template('monuments.html', title='Skulptuurid', entries=items)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateEntryForm()
    if form.validate_on_submit():
        d = {'name': form.name.data.strip(), 
            'creator': form.creator.data.strip(),
            'comment': form.comment.data.strip(),
            'links': form.links.data.strip(),
            'built': form.built.data,
            'multiple': form.multiple.data,
            'reg_id': form.reg_id.data.strip(),
            'osm_id': form.osm_id.data.strip(),
            'wikidata': form.wikidata.data.strip(),
            'genre': form.genre.data.strip(),
            'lat': form.lat.data,
            'lon': form.lon.data,
            'width_cm': form.width_cm.data,
            'length_cm': form.length_cm.data,
            'height_cm': form.height_cm.data,
            'last_seen': form.last_seen.data,
            'country': form.country.data.strip(),
            'locality': form.locality.data.strip(),
            'address': form.address.data.strip(),
            'zip_code': form.zip_code.data.strip()
        }
        if form.photos.data:
            d['photos'] = form.photos.data

        if form.order.data:
            d['order'] = form.order.data

        MonumentService.post_monument(d)

        return redirect(url_for('monuments'))

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
        user = UserService.get_user_by_username(form.username.data.strip())
        if user is None or not user.check_password(form.password.data.strip()): # verify password
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
        d = {'username': form.username.data.strip(), 
            'email': form.email.data.strip(),
            'full_name': form.full_name.data.strip(),
            'password': form.password.data.strip()
        }
        UserService.post_user(d)
        flash('Kasutaja loomine õnnestus!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Registreeru', form=form)
