from flask import make_response, current_app
from flask_login import login_user, current_user
from werkzeug.utils import secure_filename
import sqlalchemy as sa
from sqlalchemy.orm import joinedload, load_only
from PIL import Image
import cloudinary.uploader
import cloudinary.exceptions
from datetime import datetime
import uuid
import os
from app import db
from app.models import User, Monument, Photo


class UserService():
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

        # current_app.logger.info('[!] New user registration: %s - %s', user.username, user.full_name, user.email)
        new_user_id = user.id

        db.session.add(user)
        db.session.commit()
        return new_user_id


class MonumentService():
    @staticmethod
    def post_monument(data):
        """Create and save new monument entry from given data"""
        data['user_id'] = current_user.id
        exclude = {"photos", "order"}

        monument = Monument(**{k: v for k, v in data.items() if k in Monument.__table__.columns and k not in exclude and v is not None})

        db.session.add(monument)
        db.session.flush()

        for photo in data['photos']:
            # TODO order

            pdata = {'file': photo, 'monument_id': monument.id}
            new_photo = PhotoService.post_photo_and_flush(pdata)
            monument.gallery.append(new_photo)

        # current_app.logger.info('[!] New monument entry: %s, created by: %s', monument.name, current_user.username)
        new_monument_id = monument.id

        db.session.commit()
        return new_monument_id

    @staticmethod
    def get_all_monuments_with_photos():
        """Fetch and return all monuments, excluding photo keys and filename fields"""
        items = db.session.scalars(db.select(Monument).order_by(Monument.created_at.desc())).all()
        result = []
        for m in items:
            result.append({
                "id": m.id,
                "name": m.name, "creator": m.creator,
                "comment": m.comment, "links": m.links,
                "built": m.built, "multiple": m.multiple,
                "reg_id": m.reg_id, "osm_id": m.osm_id,
                "wikidata": m.wikidata, "genre": m.genre,
                "country": m.country, "locality": m.locality,
                "address": m.address, "zip_code": m.zip_code,
                "lat": m.lat, "lon": m.lon,
                "width_cm": m.width_cm, "length_cm": m.length_cm,
                "height_cm": m.height_cm, "last_seen": m.last_seen,
                "removed": m.removed, "uploader": m.uploader.username,
                "created_at": m.created_at, "last_edit": m.last_edit,
                "needs_info": m.needs_info, "needs_photos": m.needs_photos,
                "gallery": [{"id": p.id, "thumb_url": p.thumb_url, 
                            "full_url": p.full_url, "caption": p.caption} 
                            for p in m.gallery]
            })
        return result

    @staticmethod
    def get_all_monuments_locations():
        """Fetch and return all monuments for drawing on a map"""
        cols = [Monument.id, Monument.lat, Monument.lon, Monument.name]
        items = db.session.execute(db.select(*cols).order_by(Monument.created_at.desc())).all()
        result = []
        for m in items:
            result.append({
                "id": m.id,
                "name": m.name,
                "lat": m.lat,
                "lon": m.lon
            })
        return result


class PhotoService():
    @staticmethod
    def generate_safe_filename(fname):
        orig_filename = secure_filename(fname)
        dt = datetime.now().strftime("%Y%m%d")
        uid = str(uuid.uuid4())[:8]
        filename =  f'{dt}-{uid}.{orig_filename.split(".")[-1]}'
        return filename

    @staticmethod
    def upload_to_cloudinary(fpath, folder):
        upload_result = cloudinary.uploader.upload(fpath, resource_type="image", folder=folder)
        furl = upload_result["secure_url"]
        fkey = upload_result["public_id"]
        assert furl
        assert fkey
        # current_app.logger.info('Uploaded image to cloudinary: %s', fkey)
        return (furl, fkey)

    @staticmethod
    def cleanup_tmp_file(fpath):
        try:
            os.remove(fpath)
        except OSError as e:
            pass
            # current_app.logger.info('Failed to delete temporary image files from /tmp: %s', e)

    @staticmethod
    def upload_thumbnail(f, folder='/thumb'):
        filename =  PhotoService.generate_safe_filename(f.filename)
        tpath = f'/tmp/webapp/flask_upload_servicer/cloudinary/thumb_{filename}'

        with Image.open(f) as im:
            im.thumbnail(current_app.config['THUMB_SIZE'])
            im.save(tpath, "JPEG")
            # current_app.logger.info('Saved resized thumbnail to tmp path: %s', tpath)

        thumb_url, thumb_key = PhotoService.upload_to_cloudinary(tpath, folder)
        PhotoService.cleanup_tmp_file(tpath)

        return (thumb_url, thumb_key)

    @staticmethod
    def upload_photo(f, folder='/fullimg'):
        filename =  PhotoService.generate_safe_filename(f.filename)
        tpath = f'/tmp/webapp/flask_upload_servicer/cloudinary/fullimg_{filename}'

        with Image.open(f) as im:
            im.save(tpath, "JPEG")
            # current_app.logger.info('Saved full image to path: %s', tpath)

        img_url, img_key = PhotoService.upload_to_cloudinary(tpath, folder)
        PhotoService.cleanup_tmp_file(tpath)

        return (img_url, img_key)

    @staticmethod
    def post_photo_and_flush(data):
        """
        Create a new photo entry, flush it and return newly created object.
        Session MUST BE committed later.
        """
        thumb_url, thumb_key = PhotoService.upload_thumbnail(data['file'], '/tmp_photo_thumb_sculptar_entry')
        img_url, img_key = PhotoService.upload_photo(data['file'], '/tmp_photo_fullimg_sculptar_entry')
        
        photo = Photo(thumb_key=thumb_key, 
                      thumb_url=thumb_url, 
                      full_key=img_key, 
                      full_url=img_url,
                      filename=data['file'].filename,
                      monument_id=data['monument_id'],
                      user_id=current_user.id)

        # current_app.logger.info('[!] New photo entry: %s for monument %s', photo.id, photo.monument_id)

        db.session.add(photo)
        db.session.flush()
        return photo


