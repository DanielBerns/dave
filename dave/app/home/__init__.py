# your_project_name/app/home/__init__.py

from flask import Blueprint

# Note: No template_folder specified here, it will look in the global app/templates/
# Or you can specify template_folder='templates' and put templates in app/home/templates/home/
bp = Blueprint('home', __name__)

# Import routes at the bottom
from . import routes

# --- your_project_name/app/home/routes.py ---

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from . import bp # Import from current package
from ..models import Resource # Import Resource model

@bp.route('/')
@bp.route('/index')
# @login_required # Uncomment this if the home page should require login
def index():
    """Renders the home page."""
    # Example: Get some resources to display
    # In a real app, you might paginate or filter these
    resources = Resource.query.order_by(Resource.timestamp.desc()).limit(10).all()

    # You can pass user information and resources to the template
    return render_template('home/index.html', title='Home', user=current_user, resources=resources)

# Add other routes for the home section as needed
# For example, a route to view a specific resource:
@bp.route('/resource/<int:resource_id>')
def view_resource(resource_id):
    """Displays a specific resource."""
    resource = Resource.query.get_or_404(resource_id)

    if resource.resource_type == ResourceType.HTML:
        # Render the HTML content (potentially using a specific template or directly)
        # Be cautious about rendering user-submitted HTML directly (XSS risk)
        # Consider sanitizing or using a template engine carefully
        # For now, just pass the content
        return render_template('home/view_html_resource.html', title=resource.name, resource=resource)
    elif resource.resource_type == ResourceType.IMAGE:
        # Render a page that displays the image
        return render_template('home/view_image_resource.html', title=resource.name, resource=resource)
    else:
        flash('Unknown resource type.', 'warning')
        return redirect(url_for('home.index'))

# The `home` blueprint defines the main landing page (`/` or `/index`).
# It currently retrieves the 10 most recent resources to display.
# The `@login_required` decorator can be uncommented if you want to restrict access to logged-in users.
# A basic route to view individual resources is also included
