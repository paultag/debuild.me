from debuild import app
from flask import Flask, render_template, abort


@app.route("/")
def about():
    return render_template('about.html', **{})
