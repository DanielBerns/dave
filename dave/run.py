from app import create_app, db # Import factory function and db instance
from app.models import User, TextHTML, Image # Import models

# Create the Flask app instance using the factory
app = create_app()

# Optional: Add shell context processor for 'flask shell'
# Makes 'app', 'db', 'User', 'TextHTML', 'Image' available in the shell without imports
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'TextHTML': TextHTML, 'Image': Image}

# The following block allows running the app directly using 'python run.py'
# However, using 'flask run' (which uses .flaskenv) is generally preferred
if __name__ == '__main__':
    # Consider using app.run() only for development
    # Use a production WSGI server like Gunicorn or uWSGI for deployment
    app.run(debug=True) # debug=True enables debugger and reloader

