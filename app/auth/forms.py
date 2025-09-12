from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Kasutajanimi', validators=[DataRequired()])
    password = PasswordField('Parool', validators=[DataRequired()])
    remember_me = BooleanField('Jäta mind meelde')
    submit = SubmitField('Logi sisse')


class RegistrationForm(FlaskForm):
    username = StringField('Kasutajanimi', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Nimi', validators=[DataRequired()])
    password = PasswordField('Parool', validators=[DataRequired()])
    password2 = PasswordField('Korda parool', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registreeru')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Palun vali teine kasutajanimi.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Palun kasuta teine meiliaadress.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Saada link')