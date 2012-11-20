from debuild import app
from flask import render_template


@app.route("/")
def about():
    return render_template('about.html', **{})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
