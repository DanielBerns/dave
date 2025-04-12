from flask import Blueprint

# Note: No template_folder specified here, it will look in the global app/templates/
# Or you can specify template_folder='templates' and put templates in app/home/templates/home/
bp = Blueprint('home', __name__)

# Import routes at the bottom
from app.home import routes
