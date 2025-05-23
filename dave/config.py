# dave/config.py
"""
This file sets up the basic configuration of the application.
Make sure dotenv file exists in the expected location
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from storage import Storage

BASE = str(Path("~", "Info").expanduser())
IDENTIFIER = "dave" # maybe os.environ.get('IDENTIFIER')
root, store_path, logs_path = Storage.initialize(BASE, IDENTIFIER)

# Load environment variables from .env file "{root}/.env"
print(root)
load_dotenv(Path(root, '.env'))

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + str(Path(store_path, 'app.db'))
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'DEBUG'
    ADMIN = os.environ.get('ADMIN') or 'admin'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STORE_PATH = str(store_path)
    UPLOADS_FOLDER = str(Storage.container(store_path, "images")) # Storage.container creates the folder in case it doesn't exist
    LOGS_PATH = str(logs_path)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'html'} # Allowed file types

# --- requirements.txt ---
# Create a file named requirements.txt in the root directory
# List all project dependencies here.
# Example requirements.txt content:
# Flask>=2.0
# Flask-SQLAlchemy>=2.5
# Flask-WTF>=1.0       # For web forms
# WTForms[email]       # For email validation in forms
# python-dotenv>=0.19
# Flask-Login>=0.5     # For user session management
# Werkzeug>=2.0        # Flask dependency, ensure compatibility
# email-validator      # For email validation in WTForms
# Flask-Migrate>=3.0   # Optional: For database migrations


# These files set up the basic configuration, environment variables, and dependencies for your Flask application.
