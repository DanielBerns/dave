# your_project_name/app/models.py

from datetime import datetime
import enum

import sqlalchemy as sa
import sqlalchemy.orm as so

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db # Import db instance from app package (__init__.py)


# Enum for Resource Type
class ResourceType(enum.Enum):
    HTML = 'html'
    IMAGE = 'image'

class ImageType(enum.StrEnum):
    PNG  = '.png'
    JPG  = '.jpg'
    JPEG = '.jpeg'
    GIF  = '.gif'


class User(UserMixin, db.Model):
    """User model for authentication."""
    id = so.Mapped[int] = so.mapped_column(primary_key=True)
    username = so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email = so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash = so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) # Increased length for stronger hashes
    # Relationship to resources created by the user
    resources: so.WriteOnlyMapped['Resource'] = so.relationship(back_populates='author', lazy='dynamic')

    def set_password(self, password: str) -> None:
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> None:
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.username} at {self.email}>'


def create_resource_key() -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, "dave.org"))


class Resource(db.Model):
    """Resource model for storing HTML pages and image references."""
    id = so.Mapped[int] = so.mapped_column(primary_key=True)
    resource_type = so.Mapped[ResourceType]
    timestamp = so.Mapped[datetime] = so.mapped_column(index=True, default=datetime.utcnow)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped['User'] = so.relationship(back_populates='resources')


class HTMLResource(db.Model):
    """HTML content"""
    id = so.Mapped[int] = so.mapped_column(primary_key=True)
    key = so.Mapped[str] = so.mapped_column(sa.String(36), index=True)
    html_content = so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    resource_id = so.Mapped[int] = so.mapped_column(db.ForeignKey('Resource.id')) # Link to the resource definition

    def resource_url(self) -> str:
        return f"text_html/{self.key}"

def base_256(number: int) -> Tuple[int, int, int]:
    """
    Converts a non-negative integer to a base-256 representation.

    Args:
        number: The integer to convert (must be between 0 and 16777215 inclusive).

    Returns:
        A tuple of three integers representing the base-256 digits
        (most significant to least significant).

    Raises:
        AssertionError: If the input number is out of range.
    """
    assert 0 <= number < 16777216, f"Input number must be between 0 and 16777215. Got {number}"
    third_digit = number % 256
    number >>= 8  # Equivalent to number //= 256
    second_digit = number % 256
    first_digit = number >> 8  # Equivalent to number //= 256
    return first_digit, second_digit, third_digit


def base_10(first_digit: int, second_digit: int, third_digit: int) -> int:
    """
    Converts a three-digit base-256 number to its base-10 representation.

    Args:
        first_digit: The most significant digit (0-255).
        second_digit: The middle digit (0-255).
        third_digit: The least significant digit (0-255).

    Returns:
        The integer representation of the base-256 number.
    """
    return (((first_digit << 8) + second_digit) << 8) + third_digit


def get_number_identifier(number: int) -> Tuple[str, str, str]:
    """
    Generates a zero-padded, 9-digit string identifier from an integer.

    Args:
        number: The integer to convert (must be between 0 and 16777215 inclusive).

    Returns:
        Three 3-character strings representing the identifier (e.g., "000000000", "001002003").
    """
    first_digit, second_digit, third_digit = base_256(number)
    return (f"{first_digit:03d}", f"{second_digit:03d}", f"{third_digit:03d}")


class IMAGEResource(db.Model):
    id = so.Mapped[int] = so.mapped_column(primary_key=True)
    key = so.Mapped[str] = so.mapped_column(sa.String(36), index=True)
    resource_id = so.Mapped[int] = so.mapped_column(sa.ForeignKey('Resource.id')) # Link to the resource definition
    image_type = so.Mapped[ImageType]

    def filepath(self) -> Path:
        first_digit, second_digit, third_digit = get_number_identifier(self.id)
        return Path(app.config["IMAGES_FOLDER"], first_digit, second_digit, third_digit, "image").with_suffix(str(self.image_type))

    def resource_url(self) -> str:
        return f"image/{self.key}"

    def __repr__(self):
        return f'<Image {self.id} - {self.resource_id} - ({str(self.image_type)})>'

    # Potential helper methods:
    # def get_image_url(self):
    #     if self.resource_type == ResourceType.IMAGE and self.filepath:
    #         # Construct URL based on UPLOAD_FOLDER configuration and filepath
    #         # Requires access to app config or defining static URL path
    #         pass
    #     return None

# These are the SQLAlchemy models for your `User` and `Resource` tables.
# The `User` model includes password hashing and methods required by Flask-Login.
# The `Resource` model stores information about uploaded HTML content or image files.
