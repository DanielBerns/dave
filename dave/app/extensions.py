from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions, but don't configure them yet
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
