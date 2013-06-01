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

from flask import Blueprint, render_template
from lucy import Source

from humanize import naturaltime
import datetime as dt


frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.app_template_filter('seconds_display')
def seconds_display(time):
    td = timedelta(seconds=time)
    return naturaltime(td)


@frontend.app_template_filter('ago')
def ago_display(when):
    if when is None:
        return "never"
    td = dt.datetime.utcnow() - when
    return naturaltime(td)


@frontend.route("/")
def index():
    return render_template('about.html')


@frontend.route("/sources")
def source_list():
    sources = Source.query({})
    return render_template('source_list.html', **{
        "sources": sources
    })


@frontend.route("/source/<package_id>")
def source(package_id):
    package = Source.load(package_id)
    return render_template('source.html', **{
        "package": package
    })
