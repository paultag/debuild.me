import hashlib
from monomoy.core import db
from humanize import naturalday, naturalsize
from bson.objectid import ObjectId

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
def index():
    return render_template('index.html', **{})


@site.route("/about")
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


@site.app_template_filter('md5hash')
def _hash_email(obj):
    return hashlib.md5(obj).hexdigest()


@site.app_template_filter('humanize_date')
def _humanize_date_filter(obj):
    return naturalday(obj)


@site.app_template_filter('humanize_size')
def _humanize_size_filter(obj):
    return naturalsize(obj)


@site.app_template_filter('display_name')
def _display_name_filter(obj):
    user = db.users.find_one({"_id": obj})
    if user is None:
        user = db.users.find_one({"_id": ObjectId(obj)})
    return "{first_name} {last_name}".format(**user)


@site.app_template_filter('job_status_string')
def _job_status_string(job):
    severities = [
        "undefined",
        "ok",
        "info",
        "warning",
        "error"
    ]
    checks = [x['severity'] for x in
              db.checks.find({"job": job['_id']})]
    idex = 0
    for check in checks:
        n_idex = severities.index(check)
        if n_idex > idex:
            idex = n_idex
    return severities[idex]


@site.app_template_filter('job_name')
def _job_name_filter(obj):
    job = db.jobs.find_one({"_id": obj})
    if job is None:
        job = db.job.find_one({"_id": ObjectId(obj)})
    if job is None:
        return obj
    return "{type}".format(**job)


@site.app_template_filter('build_status')
def _job_name_filter(obj):
    total = db.jobs.find({"package": obj['_id']}).count()
    finished = db.jobs.find({"package": obj['_id'],
                             "finished": True}).count()

    todo = total - finished

    return "%s builds (%s remain)" % (total, todo)


@site.app_template_filter('package_name')
def _package_name_filter(obj):
    package = db.packages.find_one({"_id": obj})
    if package is None:
        package = db.packages.find_one({"_id": ObjectId(obj)})
    if package is None:
        return obj
    return "{Source}/{Version}".format(**package['changes'])
