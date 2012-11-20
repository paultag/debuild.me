from debuild import app
from flask import render_template, abort

API_BASE = '/api'


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
    pass
