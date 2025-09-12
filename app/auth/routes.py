from flask import abort, render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm
from app.models import User, Monument, Photo
# from flask_babel import _
from math import ceil
import random
import os
import uuid
import json
from app.services import UserService


@bp.route('/logout')
# @login_required
def logout():
    logout_user()
    flash('Olete välja logitud')
    return redirect(url_for('main.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exists
        user = UserService.get_user_by_username(form.username.data.strip())
        if user is None or not user.check_password(form.password.data.strip()): # verify password
            flash('Vale kasutajanimi või parool')
            return redirect(url_for('auth.login'))

        # app.logger.info('Logging in user %s', user.username)
        UserService.log_user_in(user, form.remember_me.data)

        # Redirect to original page, or index
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')

        return redirect(next_page)

    return render_template('auth/login.html', title='Logi sisse', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        d = {'username': form.username.data.strip(), 
            'email': form.email.data.strip(),
            'full_name': form.full_name.data.strip(),
            'password': form.password.data.strip()
        }
        UserService.post_user(d)
        flash('Kasutaja loomine õnnestus!')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registreeru', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        # if user:
            # send_password_reset_email(user)
        # flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html', title='Parooli taastamine', form=form)
