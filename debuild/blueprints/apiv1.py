# Copyright (c) 2012 Paul Tagliamonte <paultag@debian.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from chatham.builders import (Builder, ChathamBuilderNotFound,
                              ChathamSanityException)
from storz.decompress import digest_firehose_tree
from monomoy.core import db
from firehose.report import Analysis
from debuild import __version__

from flask import Blueprint, request, abort

from functools import wraps
import StringIO
import json


api = Blueprint('apiv1', __name__, template_folder='templates')


def _jr(obj, hr_status="ok", status=200):
    """
    Return a JSON response
    """
    obj['status'] = hr_status

    return (json.dumps(obj), status, {
        "X-Debuild-Version": __version__,
        "X-Why-Quote": "Keep your producer guessing, when you're in "
                       "the booth confessing"
    })


def protected(fn):
    """
    Protect an API method
    """
    @wraps(fn)
    def _(*args, **kwargs):
        buildd_name = request.form['name']
        buildd_token = request.form['signature']

        node = Builder(buildd_name)
        node.ping()

        if node.validate_request(buildd_token):
            return apimethod(fn)(*args, **kwargs)
        else:
            return _jr({
                "message": "Invalid Token"
            }, "failure", 401)
    return _


def apimethod(fn):
    """
    This is an API method. Catch common errors.
    """
    def _(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ChathamBuilderNotFound:
            return _jr({
                "message": "No such buildd node known."
            }, "failure", 401)
        except ChathamSanityException:
            return _jr({
                "message": "General sanity error. WTF did you do?"
            }, "failure", 501)
    return _


@api.route("/")
def index():
    """
    Say hi!
    """
    return "Hello!"


@api.route("/token", methods=["POST"])
@apimethod
def token():
    """
    Request a token to sign the next response with. This is an unprotected
    method.
    """
    buildd_name = request.form['name']
    node = Builder(buildd_name)
    tok = node.new_token()
    return _jr({"token": tok})


@api.route("/ping", methods=["POST"])
@protected
def ping():
    """
    Basically, a no-op. Test of the proecteted method stuff.
    """
    buildd_name = request.form['name']
    node = Builder(buildd_name)
    node.ping()
    return _jr({"ping": "ok"})


@api.route("/log", methods=["POST"])
@protected
def log():
    """
    Post a build log (in Firehose) format to the internal DB.

    name::
        package ID that the log relates to

    firehose::
        firehose XML payload containing the build results.
    """
    buildd_name = request.form['name']
    node = Builder(buildd_name)
    report = Analysis.from_xml(StringIO.StringIO(request.form['firehose']))
    entry = digest_firehose_tree(report)
    db.reports.insert({
        "package": request.form['package'],
        "log": entry
    }, safe=True)
    return _jr({"log": "ok"})
