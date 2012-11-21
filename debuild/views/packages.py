from debuild import app
from monomoy.core import db
from bson.objectid import ObjectId
from debuild.utils import db_find

from flask import render_template, abort


@app.route("/packages")
def packages():
    return render_template('packages.html', **{
        "packages": db.packages.find()
    })


@app.route("/package/<package_id>")
def package(package_id):
    package = db_find('packages', package_id)
    if package is None:
        abort(404)

    closes = []  # refactor this into Changes' object
    if 'Closes' in package['changes']:
        closes = [x.strip() for x in package['changes']['Closes'].split()]

    return render_template('package.html', **{
        "closes": closes,
        "package": package,
        "user": db.users.find_one({"_id": package['user']}),
        "jobs": db.jobs.find({"package": package['_id']})
    })
