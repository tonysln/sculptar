from flask import abort, render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from app import db
from app.main.forms import CreateEntryForm
from app.models import User, Monument, Photo
# from flask_babel import _
from math import ceil
import random
import os
import uuid
import json
from app.services import MonumentService
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Kodu')


@bp.route('/map')
def map():
    items = MonumentService.get_all_monuments_locations()
    return render_template('map.html', title='Kaart', entries=items)


@bp.route('/monuments')
def monuments():
    items = MonumentService.get_all_monuments_with_photos()
    return render_template('monuments.html', title='Skulptuurid', entries=items)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateEntryForm()
    if form.validate_on_submit() and current_user.is_authenticated:
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

        return redirect(url_for('main.monuments'))

    return render_template('create.html', title='Lisa uus skulptuur', form=form)


@bp.route('/account')
@login_required
def account():
    return render_template('account.html', title='Konto')


@bp.route('/admin')
@login_required
def admin():
    return render_template('admin.html', title='Admin')

