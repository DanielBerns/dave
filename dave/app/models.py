from datetime import datetime
import enum
from pathlib import Path
import secrets
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.extensions import db, login_manager
from app.tools import get_identifiers_from_number


# Enum for Resource Type
class ResourceType(enum.StrEnum):
    TEXT_HTML = 'text_html'
    IMAGE = 'image'


class ImageType(enum.StrEnum):
    PNG  = '.png'
    JPG  = '.jpg'
    JPEG = '.jpeg'
    GIF  = '.gif'


class User(UserMixin, db.Model):
    """User model for authentication."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) # Increased length for stronger hashes
    token: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), index=True, unique=True)
    token_expiration: so.Mapped[Optional[datetime]]

    # Relationship to resources created by the user
    text_htmls: so.WriteOnlyMapped['TextHTML'] = so.relationship(back_populates='author', lazy='dynamic')
    images: so.WriteOnlyMapped['Image'] = so.relationship(back_populates='author', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username} at {self.email}>'

    def url(self) -> str:
        return url_for('api.user', id=self.id)

    def text_htmls_url(self) -> str:
        return url_for('api.text_htmls', id=self.id),

    def images_url(self) -> str:
        return url_for('api.images', id=self.id),

    def set_password(self, password: str) -> None:
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> None:
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def text_htmls_count(self) -> int:
        return 0

    def images_count(self) -> int:
        return 0

    def to_dict(self) -> dict[str, str]:
        data = {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'text_htmls_count': str(self.text_htmls_count()),
            'images_count': str(self.images_count()),
            'links': {
                'self': self.url(),
                'text_htmls': self.text_htmls_url(),
                'images': self.images_url()
            }
        }
        return data

    def get_token(self, expires_in: int = 3600) -> str:
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(tzinfo=timezone.utc) > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        return self.token

    def revoke_token(self) -> None:
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)
        db.session.commit()



@login_manager.user_loader
def load_user(id: int) -> User:
    return db.session.get(User, int(id))


class TextHTML(db.Model):
    """Text HTML content"""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    label: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped['User'] = so.relationship(back_populates='text_htmls')

    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<TextHTML({self.id}, {self.timestamp}, {self.author.username}, {self.label})>'

    def url(self) -> str:
        return f"{str(ResourceType.TEXT_HTML)}/{self.label}"

    def mimetype(self) -> str:
        return "mimetype"

    def to_dict(self) -> dict[str, str]:
        data = {
            'id': str(self.id),
            'label': self.label,
            'timestamp': str(self.timestamp),
            'mimetype': self.mimetype(),
            'links': {
                'self': self.url(),
                'author': self.author.url()
            }
        }
        return data




class Image(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    label: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    count: so.Mapped[int]
    image_type: so.Mapped[ImageType]

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped['User'] = so.relationship(back_populates='images')

    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=datetime.utcnow)

    def filepath(self) -> Path:
        first_identifier, second_identifier, third_identifier = get_identifiers_from_number(self.cursor)
        name = f"{first_identifier}{second_identifier}{third_identifier}"
        return Path(app.config["IMAGES_FOLDER"], first_identifier, second_identifier, name).with_suffix(str(self.image_type))

    def __repr__(self) -> str:
        return f'<Image({self.id}, {self.timestamp}, {self.author.username}, {self.label}, {self.cursor}, {str(self.image_type)})>'

    def url(self) -> str:
        return f"{str(ResourceType.IMAGE)}/{self.label}"

    def mimetype(self) -> str:
        return "mimetype"

    def to_dict(self) -> dict[str, str]:
        data = {
            'id': str(self.id),
            'label': self.label,
            'timestamp': str(self.timestamp),
            'mimetype': self.mimetype(),
            'links': {
                'self': self.url(),
                'author': self.author.url()
            }
        }
        return data
