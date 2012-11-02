# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

from flask import Flask, render_template
from monomoy.core import db

app = Flask(__name__)


@app.route("/")
def about():
    return render_template('about.html', **{})


@app.route("/packages")
def packages():
    packages = db.packages.find()
    return render_template('packages.html', **{
        "packages": packages
    })


if __name__ == "__main__":
    app.debug = True
    app.run()
