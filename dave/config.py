# your_project_name/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env')) # Go up one level to find .env

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'app.db') # Store db outside app folder
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'html', 'htm'} # Allowed file types

    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Optional: Add other configurations like mail server, etc.

# --- .env ---
# Create a file named .env in the root directory (your_project_name/)
# Add your secret key and database URL here.
# Example .env content:
# SECRET_KEY=a_very_strong_and_random_secret_key
# DATABASE_URL=sqlite:///../app.db # Or postgresql://user:password@host:port/dbname
# UPLOAD_FOLDER=app/static/uploads

# --- .flaskenv ---
# Create a file named .flaskenv in the root directory
# This tells Flask how to run the app.
# Example .flaskenv content:
# FLASK_APP=run.py
# FLASK_ENV=development # Use 'production' in production

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
```
# These files set up the basic configuration, environment variables, and dependencies for your Flask application.
