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

from flask import Blueprint, render_template, send_file
from lucy import Source, Report, Machine, User, Job
from lucy.core import get_config
from fred import db as fred_db

from humanize import naturaltime
from humanize.time import naturaldelta

from datetime import timedelta
import datetime as dt
import os.path


frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.app_template_filter('seconds_display')
def seconds_display(time):
    td = timedelta(seconds=time)
    return naturaldelta(td)


@frontend.app_template_filter('ago')
def ago_display(when):
    if when is None:
        return "never"
    td = dt.datetime.utcnow() - when
    return naturaltime(td)


@frontend.app_template_filter('location')
def location_display(obj):
    if obj is None:
        return ""

    fo = obj['file']
    po = obj['point']

    if po is None:
        return fo['givenpath']

    return "%s:%s" % (obj['file']['givenpath'],
                      obj['point']['line'])


@frontend.route("/")
def index():
    active_jobs = Job.unfinished_jobs()
    pending = fred_db.builds.find()
    return render_template('about.html', **{
        "active_jobs": active_jobs,
        "machines": Machine.get_builders(),
        "fred_builds": pending,
    })


@frontend.route("/sources/")
def source_list():
    count = 10
    sources = Source.query({}, sort='updated_at', sort_order=-1, limit=count)
    return render_template('source_list.html', **{
        "sources": sources,
        "count": count,
    })


@frontend.route("/group/<group_id>/")
@frontend.route("/group/<group_id>/<page>/")
def group_list(group_id, page=0):
    page = int(page)

    sources = Source.query(
        { "group": group_id, },
        sort='updated_at',
        sort_order=1,
        page_count=15,
        page=page
    )

    return render_template('group.html', **{
        "sources": sources,
        "group_id": group_id,
        "page": page,
    })


@frontend.route("/source/<package_id>/")
def source(package_id):
    package = Source.load(package_id)
    return render_template('source.html', **{
        "package": package
    })


@frontend.route("/machine/<machine_id>/")
def machine(machine_id):
    machine = Machine.load(machine_id)
    return render_template('machine.html', **{
        "machine": machine,
        "owner": machine.get_owner()
    })


@frontend.route("/hacker/<hacker_id>/")
def hacker(hacker_id):
    user = User.load(hacker_id)
    return render_template('hacker.html', **{
        "hacker": user
    })


@frontend.route("/report/<report_id>/")
def report(report_id):
    report = Report.load(report_id)
    config = get_config()
    log_path = os.path.join(config['pool'],
                        report['log_path'])

    flink = "/report/firehose/%s/" % report_id
    loglink = "/report/log/%s/" % report_id

    log = []
    if os.path.exists(log_path):
        log = (x.decode('utf-8') for x in open(log_path, 'r'))

    return render_template('report.html', **{
        "log_link": loglink,
        "firehose_link": flink,
        "report": report,
        "log": log,
    })

@frontend.route("/report/firehose/<report_id>/")
def report_firehose(report_id):
    report = Report.load(report_id)
    config = get_config()
    firehose_path = os.path.join(config['pool'],
                        report['firehose_path'])

    if os.path.exists(firehose_path):
        return send_file(firehose_path, mimetype='application/xml', as_attachment=True, attachment_filename='firehose.xml')

@frontend.route("/report/log/<report_id>/")
def report_log(report_id):
    report = Report.load(report_id)
    config = get_config()
    log_path = os.path.join(config['pool'],
                        report['log_path'])

    if os.path.exists(log_path):
        return send_file(log_path, mimetype='text/plain', as_attachment=True, attachment_filename='log.txt')
