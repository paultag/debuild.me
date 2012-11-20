from debuild import app
from monomoy.core import db
from humanize import naturalday, naturalsize
from bson.objectid import ObjectId
import hashlib


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
