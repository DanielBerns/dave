# your_project_name/app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_migrate import Migrate # Uncomment if using Flask-Migrate
from .config import Config # Use dot notation for relative import

# Initialize extensions, but don't configure them yet
db = SQLAlchemy()
login_manager = LoginManager()
# migrate = Migrate() # Uncomment if using Flask-Migrate

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
    # migrate.init_app(app, db) # Uncomment if using Flask-Migrate

    # Import and register blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .home import bp as home_bp
    app.register_blueprint(home_bp) # No prefix, makes it the default

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Define user loader function for Flask-Login
    # Needs to be defined here or imported after User model is defined
    # We'll define it after importing models to avoid circular imports
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # Return the user object or None if not found
        return User.query.get(int(user_id))

    # Optional: Create database tables if they don't exist
    # This is simple but Flask-Migrate is better for production
    with app.app_context():
        # You might want to remove this in production and use migrations
        # db.create_all()
        # Check if upload folder exists, create if not
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            print(f"Created upload folder: {upload_folder}")


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
