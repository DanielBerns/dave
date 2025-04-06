# your_project_name/app/models.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db # Import db instance from app package (__init__.py)
import enum

# Enum for Resource Type
class ResourceType(enum.Enum):
    HTML = 'html'
    IMAGE = 'image'

class User(UserMixin, db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256)) # Increased length for stronger hashes
    # Relationship to resources created by the user
    resources = db.relationship('Resource', backref='author', lazy='dynamic')

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Resource(db.Model):
    """Resource model for storing HTML pages and image references."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False) # e.g., 'about_us.html' or 'logo.png'
    resource_type = db.Column(db.Enum(ResourceType), nullable=False)
    # For HTML: store the content directly
    html_content = db.Column(db.Text, nullable=True)
    # For Images: store the filename (image stored in UPLOAD_FOLDER)
    filepath = db.Column(db.String(256), nullable=True) # Path relative to UPLOAD_FOLDER or absolute
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Link to the user who uploaded it

    def __repr__(self):
        return f'<Resource {self.name} ({self.resource_type.name})>'

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
