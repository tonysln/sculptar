from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileRequired, FileAllowed, FileSize
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, FloatField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db, app
from app.models import User
# from flask_babel import lazy_gettext as _l


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
    photos = MultipleFileField('Photos', validators=[FileRequired(), 
                                FileSize(app.config['MAX_CONTENT_LENGTH'], 'Vähemalt üks valitud piltidest on liiga suur!'),
                                FileAllowed(app.config['UPLOAD_EXTENSIONS'], 'Üles laadida saab ainult pilte!')])

    name = StringField('Nimi', validators=[DataRequired()])
    creator = StringField('Autor', validators=[DataRequired()])
    comment = TextAreaField('Kirjeldus')
    links = TextAreaField('Lingid')

    built = DateField('Ehitatud', validators=[DataRequired()])

    multiple = BooleanField('See monument koosneb mitmest osast')
    reg_id = StringField('Kultuurimälestiste registri nr')
    osm_id = StringField('OpenStreetMap Node ID')
    wikidata = StringField('Wikidata ID')

    genre = StringField('Skulptuuri liik')
    lat = FloatField('Laiuskraad', validators=[DataRequired()])
    lon = FloatField('Pikkuskraad', validators=[DataRequired()])

    width_cm = IntegerField('Laius (cm)')
    length_cm = IntegerField('Pikkus (cm)')
    height_cm = IntegerField('Kõrgus (cm)')

    last_seen = DateField('Viimati nähtud', validators=[DataRequired()])

    country = StringField('Riik (EE)', validators=[DataRequired()])
    locality = StringField('Linn', validators=[DataRequired()])
    address = StringField('Aadress', validators=[DataRequired()])
    zip_code = StringField('Sihtnumber', validators=[DataRequired()])
    
    submit = SubmitField('Loo kirje')
    # cancel = SubmitField('Cancel')