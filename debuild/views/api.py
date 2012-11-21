from debuild import app
from monomoy.core import db
from debuild.utils import db_find

import json
import hashlib
import datetime as dt
from flask import render_template, abort, request


API_BASE = '/api'


def serialize(obj):
    return json.dumps(obj)


@app.route("%s/echo" % (API_BASE), methods=['POST'])
def echo():
    obj = request.form
    return serialize(obj)


@app.route("%s/ping" % (API_BASE), methods=['POST'])
def ping():
    obj = request.form['data']
    return serialize(obj)


@app.route("%s/token" % (API_BASE), methods=['POST', 'GET'])
def token():
    builder_name = request.form['node']
    builder = db.builders.find_one({
        "_id": builder_name
    })
    if builder is None:
        abort(401)

    entropy = dt.datetime.now().microsecond
    s = "%s-%s" % (str(entropy), builder_name)
    has = hashlib.sha256(s).hexdigest()

    builder['token'] = has
    db.builders.update({"_id": builder_name},
                       builder,
                       False,
                       safe=True)

    obj = {
        "builder": builder['_id'],
        "request_id": has
    }
    return serialize(obj)
