# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

from flask import Flask, render_template
from monomoy.db import db

app = Flask(__name__)


@app.route("/")
def about():
    return render_template('about.html', **{})


@app.route("/uploads")
def uploads():
    changes = db.changes.find()
    return render_template('changes.html', **{
        "changes": changes
    })


if __name__ == "__main__":
    app.debug = True
    app.run()
