# Add to run.py (above the `if __name__ == "__main__":` block).
# Put sitemap.xml and robots.txt in the static/ folder.
from flask import send_from_directory


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml', mimetype='application/xml')


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt', mimetype='text/plain')
