from debuild import app
from debuild.utils import db_find

import json
from flask import render_template, abort, request


API_BASE = '/api'


@app.route("%s/echo" % (API_BASE), methods=['POST'])
def echo():
    obj = request.form
    return json.dumps(obj)


@app.route("%s/ping" % (API_BASE), methods=['POST'])
def ping():
    """
    methods: POST
    Required fields:

        - data
        - signature

    Signature:

        sha256 of:
            "%s-%s" % (timestamp, secret)
    """
    obj = request.form['data']
    return json.dumps(obj)
