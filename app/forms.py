from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileRequired, FileAllowed, FileSize
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, FloatField, IntegerField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, Length, Optional
import sqlalchemy as sa
from app import db, app
from app.models import User
# from flask_babel import lazy_gettext as _l


def order_validator(form, field):
    legal_chars = '1234567890,'
    for c in field.data:
        if c not in legal_chars:
            raise ValidationError('Piltide järjekord vigane! Palun võta ühendust administraatoriga.')


class LoginForm(FlaskForm):
    username = StringField('Kasutajanimi', validators=[DataRequired()])
    password = PasswordField('Parool', validators=[DataRequired()])
    remember_me = BooleanField('Jäta mind meelde')
    submit = SubmitField('Logi sisse')


class RegistrationForm(FlaskForm):
    username = StringField('Kasutajanimi', validators=[DataRequired()])
    email = StringField('Meil', validators=[DataRequired(), Email()])
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


class CreateEntryForm(FlaskForm):
    photos = MultipleFileField('Photos')
    order = HiddenField('Order', validators=[order_validator])

    name = StringField('Nimi', validators=[DataRequired()])
    creator = StringField('Autor', validators=[DataRequired()])
    comment = TextAreaField('Kirjeldus')
    links = TextAreaField('Lingid')

    built = DateField('Püstitatud', validators=[DataRequired()])

    multiple = BooleanField('See monument koosneb mitmest osast')
    reg_id = StringField('Kultuurimälestiste registri nr')
    osm_id = StringField('OpenStreetMap Node ID')
    wikidata = StringField('Wikidata ID')

    genre = StringField('Skulptuuri liik')
    lat = FloatField('Laiuskraad', validators=[DataRequired(), NumberRange(min=-90, max=90)])
    lon = FloatField('Pikkuskraad', validators=[DataRequired(), NumberRange(min=-180, max=180)])

    width_cm = IntegerField('Laius (cm)', validators=[Optional()])
    length_cm = IntegerField('Pikkus (cm)', validators=[Optional()])
    height_cm = IntegerField('Kõrgus (cm)', validators=[Optional()])

    last_seen = DateField('Viimati nähtud', validators=[DataRequired()])

    country = StringField('Riik', validators=[DataRequired(), Length(min=2, max=3, message="Riigikood on vale!")])
    locality = StringField('Linn', validators=[DataRequired()])
    address = StringField('Aadress', validators=[DataRequired()])
    zip_code = StringField('Sihtnumber', validators=[DataRequired(), Length(min=2, max=15, message="Sihtnumbri kuju on ebakorrektne!")])
    
    submit = SubmitField('Loo kirje')
    # cancel = SubmitField('Cancel')