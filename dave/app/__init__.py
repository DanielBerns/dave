import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

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
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.api import bp as api_bp
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

    @app.route('/test')
    def test_page():
        return '<h1>Testing the Flask Application Factory</h1>'

    return app































# Import models at the bottom to avoid circular dependencies with blueprints
# Although models don't directly import blueprints, routes within blueprints import models.
from app import models
