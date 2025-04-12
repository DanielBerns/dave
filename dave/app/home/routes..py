from flask import render_template
from app.home import bp

@bp.route('/')
@bp.route('/index')
def index():
    """Renders the home page."""
    # You can pass user information and resources to the template
    return render_template('home/index.html')
