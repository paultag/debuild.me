# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

from flask import Flask, render_template, abort
from humanize import naturalday, naturalsize
from bson.objectid import ObjectId
import hashlib

from monomoy.core import db

app = Flask(__name__)


@app.route("/")
def about():
    return render_template('about.html', **{})


@app.route("/packages")
def packages():
    return render_template('packages.html', **{
        "packages": db.packages.find()
    })


@app.route("/package/<package_id>")
def package(package_id):
    package = db.packages.find_one({"_id": package_id})

    if package is None:
        package = db.packages.find_one({"_id": ObjectId(package_id)})

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


@app.route("/check/<check_id>")
def check(check_id):
    check = db.checks.find_one({"_id": check_id})
    if check is None:
        check = db.checks.find_one({"_id": ObjectId(check_id)})

    if check is None:
        abort(404)

    return render_template('check.html', **{
        "check": check
    })


@app.route("/job/<job_id>")
def job(job_id):
    job = db.jobs.find_one({"_id": job_id})
    if job is None:
        job = db.jobs.find_one({"_id": ObjectId(job_id)})
    if job is None:
        abort(404)

    # XXX: Refactor all this garbage.

    return render_template('job.html', **{
        "job": job,
        "checks": db.checks.find({"job": job['_id']})
    })


@app.route("/user/<user_id>")
def user(user_id):
    user = db.users.find_one({"_id": user_id})
    if user is None:
        user = db.users.find_one({"_id": ObjectId(user_id)})

    if user is None:
        abort(404)

    return render_template('user.html', **{
        "user": user,
        "packages": db.packages.find({"user": user['_id']})
    })

# Error pages, etc.


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Template filters, etc.


@app.template_filter('md5hash')
def _hash_email(obj):
    return hashlib.md5(obj).hexdigest()


@app.template_filter('humanize_date')
def _humanize_date_filter(obj):
    return naturalday(obj)


@app.template_filter('humanize_size')
def _humanize_size_filter(obj):
    return naturalsize(obj)


@app.template_filter('display_name')
def _display_name_filter(obj):
    user = db.users.find_one({"_id": obj})
    if user is None:
        user = db.users.find_one({"_id": ObjectId(obj)})
    return "{first_name} {last_name}".format(**user)


if __name__ == "__main__":
    app.debug = True
    app.run()
