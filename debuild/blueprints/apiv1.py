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

from chatham.builders import Builder, ChathamBuilderNotFound
from debuild import __version__

from flask import Blueprint, request, abort

from functools import wraps
import json


api = Blueprint('apiv1', __name__, template_folder='templates')


def _jr(obj, hr_status="ok", status=200):
    obj['status'] = hr_status

    return (json.dumps(obj), status, {
        "X-Debuild-Version": __version__,
        "X-Why-Quote": "Keep your producer guessing, when you're in "
                       "the booth confessing"
    })


def protected(fn):
    @wraps(fn)
    def _(*args, **kwargs):
        buildd_name = request.form['builder_name']
        buildd_token = request.form['builder_token']

        node = Builder(buildd_name)

        return fn(*args, **kwargs)
    return _


def apimethod(fn):
    def _(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ChathamBuilderNotFound:
            return _jr({
                "message": "No such buildd node known."
            }, "failure", 401)
    return _


@api.route("/")
def index():
    return "Hello!"


@api.route("/new-token", methods=["POST"])
@apimethod
def new_token():
    buildd_name = request.form['builder_name']
    node = Builder(buildd_name)
    tok = node.new_token()
    return _jr({"token": tok})
