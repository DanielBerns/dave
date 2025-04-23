from flask import render_template

from app.home import bp

@bp.route('/')
@bp.route('/index')
def index():
    """Renders the home page."""
    return render_template('home/index.html')

@bp.route('/help')
def help():
    """Renders the help page."""
    return render_template('home/help.html')

@bp.route('/cover')
def cover():
    """Renders the cover page."""
    return render_template('home/cover.html')
