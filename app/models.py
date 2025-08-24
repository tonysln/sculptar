from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    id:            so.Mapped[int] = so.mapped_column(primary_key=True)
    username:      so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    full_name:     so.Mapped[str] = so.mapped_column(sa.String(240))
    email:         so.Mapped[str] = so.mapped_column(sa.String(240), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    entries:       so.Mapped[list["Monument"]] = so.relationship(back_populates="uploader")

    is_admin:      so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    created_at:    so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())
    last_login:    so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())


    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Monument(db.Model):
    id:        so.Mapped[int] = so.mapped_column(primary_key=True)

    # Name, description
    name:      so.Mapped[str] = so.mapped_column(sa.String(500), index=True)
    creator:   so.Mapped[str] = so.mapped_column(sa.String(500), index=True)
    comment:   so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    links:     so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    built:     so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), index=True)

    # Identification
    multiple:  so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False) # is group of monuments?
    # Estonian cultural monument ID:
    reg_id:    so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), nullable=True, index=True, unique=True)
    # OpenStreetMap node ID:
    osm_id:    so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), nullable=True, unique=True)
    wikidata:  so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), nullable=True, unique=True)
    genre:     so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), nullable=True) # ?

    # Location
    country:   so.Mapped[str] = so.mapped_column(sa.String(10), default="EE") # ISO 3166
    locality:  so.Mapped[str] = so.mapped_column(sa.String(120)) # City/Town
    address:   so.Mapped[str] = so.mapped_column(sa.String(240)) # Street + building level
    zip_code:  so.Mapped[str] = so.mapped_column(sa.String(100)) # ZIP
    lat:       so.Mapped[float] = so.mapped_column(sa.REAL)
    lon:       so.Mapped[float] = so.mapped_column(sa.REAL)

    # Size
    width_cm:  so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    length_cm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    height_cm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)

    # Last physical sighting
    last_seen: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())

    gallery: so.Mapped[list["Photo"]] = so.relationship(
        back_populates="monument",
        cascade="all, delete-orphan"
    )

    # New monument ID in case of relocation
    moved_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("monument.id"))
    moved_to: so.Mapped[Optional["Monument"]] = so.relationship(
        "Monument",
        remote_side=[id],
        back_populates="moved_from",
        uselist=False
    )
    moved_from: so.Mapped[Optional["Monument"]] = so.relationship(
        "Monument",
        # remote_side=[moved_id],
        back_populates="moved_to",
        uselist=False
    )
    # If completely removed/missing, no new entry
    removed:   so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    # Uploader account and misc metadata
    user_id:    so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    uploader:   so.Mapped["User"] = so.relationship(back_populates="entries")
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())
    last_edit:  so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())

    needs_info: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    needs_photos: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    def __repr__(self):
        return f'<Monument "{self.name}": {self.creator}>'


class Photo(db.Model):
    id:          so.Mapped[int] = so.mapped_column(primary_key=True)
    caption:     so.Mapped[str] = so.mapped_column(sa.Text)

    thumb_key:   so.Mapped[str] = so.mapped_column(sa.String(512))
    full_key:    so.Mapped[str] = so.mapped_column(sa.String(512))
    filename:    so.Mapped[str] = so.mapped_column(sa.String(512))
    orig_fname:  so.Mapped[str] = so.mapped_column(sa.String(512))
    thumb_url:   so.Mapped[Optional[str]] = so.mapped_column(sa.String(512), default="")
    full_url:    so.Mapped[Optional[str]] = so.mapped_column(sa.String(512), default="")

    monument_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Monument.id))
    user_id:     so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    monument:    so.Mapped["Monument"] = so.relationship(
        "Monument",
        back_populates="gallery",
        foreign_keys=[monument_id]
    )

    def __repr__(self):
        return f'<Photo #{self.id} for Monument #{self.monument_id}>'

