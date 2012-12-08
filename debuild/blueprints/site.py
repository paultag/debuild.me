from monomoy.core import db
from debuild.utils import db_find
from chatham.builders import Builder

from jinja2 import TemplateNotFound
from bson.objectid import ObjectId
from collections import defaultdict
from flask import Blueprint, render_template, abort, render_template


site = Blueprint(
    'site',
    __name__,
    template_folder='templates'
)


@site.route("/builder/<builder_id>")
def builder(builder_id):
    builder = Builder(builder_id)

    return render_template('builder.html', **{
        "builder": builder
    })


@site.route("/check/<check_id>")
def check(check_id):
    check = db_find('checks', check_id)
    if check is None:
        abort(404)

    tags = defaultdict(lambda: defaultdict(int))
    for block in check['data']:
        obj = check['data'][block]
        for ch in obj:
            tags[block][ch['tag']] += 1

    return render_template('check.html', **{
        "check": check,
        "tags": tags
    })


@site.route("/")
def about():
    return render_template('about.html', **{})


@site.route("/job/<job_id>")
def job(job_id):
    job = db_find('jobs', job_id)
    if job is None:
        abort(404)

    # XXX: Refactor all this garbage.

    return render_template('job.html', **{
        "job": job,
        "checks": db.checks.find({"job": job['_id']})
    })


@site.route("/packages")
def packages():
    return render_template('packages.html', **{
        "packages": db.packages.find()
    })


@site.route("/package/<package_id>")
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


@site.route("/user/<user_id>")
def user(user_id):
    user = db_find('users', user_id)
    if user is None:
        abort(404)

    return render_template('user.html', **{
        "user": user,
        "packages": db.packages.find({"user": user['_id']}),
        "builders": db.builders.find({"owner": user['_id']})
    })
