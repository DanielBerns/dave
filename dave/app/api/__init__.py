from flask import Blueprint

bp = Blueprint('api', __name__)

# Import routes at the bottom
from app.api import routes
