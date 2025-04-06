# your_project_name/run.py

from app import create_app, db # Import factory function and db instance
from app.models import User, Resource # Import models

# Create the Flask app instance using the factory
app = create_app()

# Optional: Add shell context processor for 'flask shell'
# Makes 'app', 'db', 'User', 'Resource' available in the shell without imports
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'Resource': Resource}

# The following block allows running the app directly using 'python run.py'
# However, using 'flask run' (which uses .flaskenv) is generally preferred
if __name__ == '__main__':
    # Consider using app.run() only for development
    # Use a production WSGI server like Gunicorn or uWSGI for deployment
    app.run(debug=True) # debug=True enables debugger and reloader


# This `run.py` file is the main entry point for your application.
# It imports the `create_app` factory, creates the app instance, and sets up a shell context for easier debugging with `flask shell`.
# You can run the development server using `flask run` (recommended) or `python run.py`
