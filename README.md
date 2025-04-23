# Flask Resource Management Website

A web application built with Python and Flask that allows users to sign up, log in, browse resources, and manage them (HTML pages and images) via a web interface and a RESTful API.

## Features

* **User Authentication:** Secure user sign-up, login, and logout functionality using Flask-Login.
* **Resource Browsing:** Logged-in users can view uploaded resources (HTML pages and images).
* **Resource Management API:** RESTful API endpoints for uploading, retrieving, updating (optional), and deleting resources.
* **Static File Serving:** Serves CSS, JavaScript, and static images.
* **Database Integration:** Uses Flask-SQLAlchemy to interact with a database (SQLite by default, configurable) for storing user and resource information.
* **Configuration Management:** Uses `.env` files for sensitive configuration and `config.py` for application settings.
* **Blueprints:** Organizes the application into logical modules (auth, home, api).

## Technology Stack

* **Backend:** Python 3
* **Framework:** Flask
* **Database ORM:** Flask-SQLAlchemy
* **Database Migrations:** Flask-Migrate (Recommended)
* **Authentication:** Flask-Login
* **Web Forms:** Flask-WTF
* **Environment Variables:** python-dotenv
* **Frontend:** HTML, CSS (Bootstrap 5), JavaScript
* **WSGI Server (Production):** Gunicorn or uWSGI (Recommended)

## Project Structure



your_project_name/
├── app/ # Main application package
│ ├── init.py # Application factory
│ ├── models.py # Database models
│ ├── config.py # Configuration classes
│ │
│ ├── auth/ # Authentication blueprint
│ ├── home/ # Home/Frontend blueprint
│ ├── api/ # API blueprint
│ │
│ ├── static/ # Static files (CSS, JS, images)
│ └── templates/ # HTML templates (Jinja2)
│
├── migrations/ # Flask-Migrate database migration scripts
├── .env # Environment variables (SECRET_KEY, DATABASE_URL) - Create this!
├── .flaskenv # Flask environment settings (FLASK_APP, FLASK_ENV) - Create this!
├── requirements.txt # Python dependencies
└── run.py # Application entry point / runner script

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd your_project_name
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    * Create a `.env` file in the project root directory.
    * Add the following variables (replace with your actual values):
        ```dotenv
        SECRET_KEY=your_very_secret_and_random_key_here
        DATABASE_URL=sqlite:///../app.db # Or your PostgreSQL/MySQL URL
        UPLOAD_FOLDER=app/static/uploads # Optional: defaults to this if not set
        ```
    * Create a `.flaskenv` file in the project root directory:
        ```dotenv
        FLASK_APP=run.py
        FLASK_ENV=development # Use 'production' for deployment
        ```

5.  **Initialize/Migrate Database:**
    * **If using Flask-Migrate (Recommended):**
        ```bash
        flask db init  # Run only once to initialize migrations
        flask db migrate -m "Initial database migration."
        flask db upgrade # Apply migrations to the database
        ```
    * **If *not* using Flask-Migrate (Simpler setup, less flexible):**
        Uncomment the `db.create_all()` line within the `create_app` function in `app/__init__.py` temporarily, run the app once (`flask run`), and then comment it back out.

6.  **Run the Application:**
    ```bash
    flask run
    ```
    The application should now be running at `http://127.0.0.1:5000/` (or the port specified by Flask).

## Usage

1.  **Web Interface:**
    * Navigate to `http://127.0.0.1:5000/` in your browser.
    * **Sign Up:** Click the "Sign Up" link and fill out the registration form.
    * **Login:** Click the "Login" link and use your credentials.
    * **Browse Resources:** Once logged in, the home page will display recent resources. Click on a resource name to view it.
    * **Upload Resources:** Use the upload form on the home page (available when logged in) to add new HTML content or image files.
    * **Delete Resources:** A delete button is available next to resources you own on the home page list.

2.  **API Endpoints:**
    * Authentication is required (uses session cookies from web login). You can test API endpoints using tools like `curl` or Postman after logging in via the web interface in the same browser session, or implement token-based auth for programmatic access.
    * **Base URL:** `http://127.0.0.1:5000/api`

    * **`GET /api/resources`**: List resources owned by the logged-in user.
        ```bash
        # Example using curl (assumes you have a valid session cookie)
        curl -b cookies.txt [http://127.0.0.1:5000/api/resources](https://www.google.com/search?q=http://127.0.0.1:5000/api/resources)
        ```

    * **`POST /api/resources/upload`**: Upload a new resource.
        * **HTML:**
            ```bash
            curl -b cookies.txt -X POST -F "name=my_page.html" -F "type=html" -F "html_content=<h1>Hello World</h1><p>This is content.</p>" [http://127.0.0.1:5000/api/resources/upload](https://www.google.com/search?q=http://127.0.0.1:5000/api/resources/upload)
            ```
        * **Image:**
            ```bash
            curl -b cookies.txt -X POST -F "name=my_image.jpg" -F "type=image" -F "file=@/path/to/your/image.jpg" [http://127.0.0.1:5000/api/resources/upload](https://www.google.com/search?q=http://127.0.0.1:5000/api/resources/upload)
            ```

    * **`GET /api/resources/<int:resource_id>`**: Get details of a specific resource.
        ```bash
        curl -b cookies.txt [http://127.0.0.1:5000/api/resources/1](https://www.google.com/search?q=http://127.0.0.1:5000/api/resources/1)
        ```

    * **`DELETE /api/resources/<int:resource_id>`**: Delete a specific resource.
        ```bash
        curl -b cookies.txt -X DELETE [http://127.0.0.1:5000/api/resources/1](https://www.google.com/search?q=http://127.0.0.1:5000/api/resources/1)
        ```
    *(Note: Managing cookies with `curl` (`-b`, `-c`) might be needed for session authentication testing).*

## Configuration

* **`config.py`**: Contains the main configuration classes (`Config`). Defines default settings and loads sensitive data from environment variables.
* **`.env`**: Stores sensitive configuration like `SECRET_KEY` and `DATABASE_URL`. **Do not commit this file to version control.**
*

First time

1. start.sh
2. run_shell.sh
3. run.sh

Reset
1. clean.sh
2. start.sh
3. run_shell.sh
4. run.sh

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
