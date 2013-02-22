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

from flask import Blueprint, render_template, abort
from humanize.time import naturaldelta
from datetime import timedelta
from bson import ObjectId
import os.path

from monomoy.core import db


frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.app_template_filter('seconds_display')
def seconds_display(time):
    td = timedelta(seconds=time)
    return naturaldelta(td)


@frontend.app_template_filter('location_display')
def seconds_display(issue):
    ret = ""
    loc = issue['location']

    if "file" in loc:
        ret += os.path.basename(loc['file']['givenpath'])

    if "point" in loc:
        ret += " @ line {line}, column {column}".format(**loc['point'])

    #if "function" in loc:
    #    ret += " ({name})".format(**loc['function'])

    return ret


@frontend.app_template_filter('package_display')
def package_display(sut):
    ret = "{name}/{version}".format(**sut)

    if "release" in sut:
        ret += "-{release}".format(**sut)

    if "buildarch" in sut:
        ret += " on {buildarch}".format(**sut)

    return ret


@frontend.route("/")
def index():
    return render_template('about.html')


@frontend.route("/report/<report_id>")
def report(report_id):
    report = db.reports.find_one({"_id": ObjectId(report_id)})
    if report is None:
        abort(404)

    return render_template('report.html', **{
        "report": report,
        "metadata": report['log']['metadata'],
        "sut": report['log']['metadata']['sut']
    })


@frontend.route("/package/<package_id>")
def package(package_id):
    objid = ObjectId(package_id)
    package = db.packages.find_one({"_id": objid})
    if package is None:
        abort(404)

    reports = db.reports.find({"package": objid})

    return render_template('package.html', **{
        "reports": reports,
        "package": package,
    })
