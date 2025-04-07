# your_project_name/app/__init__.py

import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_migrate import Migrate # Uncomment if using Flask-Migrate
from .config import Config # Use dot notation for relative import

logging_level_str_to_int = {
    "NOT_SET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARN,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# Initialize extensions, but don't configure them yet
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Configure login manager
login_manager.login_view = 'auth.login' # The endpoint name for the login page
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info' # Flash message category

def create_app(config_class=Config):
    """
    Application factory function.
    Creates and configures the Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app instance
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db) # Uncomment if using Flask-Migrate

    # Import and register blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .home import bp as home_bp
    app.register_blueprint(home_bp) # No prefix, makes it the default

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    file_handler = RotatingFileHandler(
        Path(app.config['LOGS_PATH'], 'application.log'),
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    logging_level = logging_level_str_to_int.get(app.config["LOGGING_LEVEL"], logging.DEBUG)
    file_handler.setLevel(logging_level)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging_level)
    app.logger.info("Started!")

    # Define user loader function for Flask-Login
    # Needs to be defined here or imported after User model is defined
    # We'll define it after importing models to avoid circular imports
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # Return the user object or None if not found
        return User.query.get(int(user_id))

    @app.route('/test')
    def test_page():
        return '<h1>Testing the Flask Application Factory</h1>'

    return app

# Import models at the bottom to avoid circular dependencies with blueprints
# Although models don't directly import blueprints, routes within blueprints import models.
from . import models
```

# This file defines the `create_app` function, which is the standard way to initialize a Flask application.
# It sets up configurations, initializes extensions like SQLAlchemy and Flask-Login, and registers your blueprints.
