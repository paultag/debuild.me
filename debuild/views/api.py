from debuild import app, monomoy
from debuild.utils import db_find

from chatham.builders import Builder

from monomoy.core import db
from monomoy.utils import JSONEncoder
from monomoy.archive import MonomoyArchive

import json
import datetime as dt
from flask import request

API_BASE = '/api'


def serialize(obj, allok):
    obj['status'] = 'ok' if allok else 'nokay'
    return json.dumps(obj, cls=JSONEncoder)


def api_abort(code, text):
    return serialize({
        'code': code,
        'text': text
    }, False)


def get_things():
    req = request.values
    builder = Builder(req['node'])
    builder.ping()
    return (req, builder)


def api_validate(keys):
    req = request.values
    for key in ['node', 'signature']:
        if key not in req:
            return api_abort(
                'forgotten-core-key',
                'Ah man, it looks like you forgot the core key '
                '"%s" in the request.' % (key)
            )

    for key in keys:
        if key not in req:
            return api_abort(
                'forgotten-view-key',
                'Ah man, it looks like you forgot the view-local key '
                '"%s" in the request.' % (key)
            )

    node = req['node']
    builder = Builder(node)
    if builder.validate_request(req['signature']):
        return None

    return api_abort(
        'bad-signature',
        'stupid signature value'
    )


@app.route("%s/package/<package_id>" % (API_BASE), methods=['GET', 'POST'])
def api_package(package_id):
    package = db_find('packages', package_id)
    if package is None:
        return api_abort('no-such-package',
                         'no such package: %s exists' % (package_id))

    archive = MonomoyArchive(monomoy['root'])
    path = archive.get_package_root(package['_id'])
    root = monomoy['archive']
    path = "%s/%s" % (root, path)

    dscs = filter(lambda x: x['name'].endswith('.dsc'),
                  package['changes']['Files'])
    files = ["%s/%s" % (path, x['name']) for x in dscs]

    return serialize({
        "files": files,
        "package": package['_id'],
        "package_obj": package
    }, True)


@app.route('%s/token' % (API_BASE), methods=['GET', 'POST'])
def token():
    req = request.values
    if 'node' not in req:  # no signature.
        return api_abort('nsp-node', 'No such param: node')

    (req, builder) = get_things()
    key = builder.new_token()

    return serialize({
        "token": key
    }, True)


@app.route("%s/ping" % (API_BASE), methods=['GET', 'POST'])
def ping():
    resp = api_validate([])
    if resp: return resp
    (req, builder) = get_things()

    builder.ping()

    return serialize({
        'ping': 'pung'
    }, True)


@app.route("%s/result" % (API_BASE), methods=['GET', 'POST'])
def result():
    resp = api_validate(['data'])
    if resp: return resp
    (req, builder) = get_things()

    data = json.loads(req['data'])
    job = data['job']
    jobj = db_find('jobs', job)
    data['job'] = jobj['_id']

    if jobj['builder'] is None:
        return api_abort('bad-builder', 'bad builder node')

    if jobj['builder'] != builder._obj['_id']:  # XXX: Fixme
        return api_abort('bad-builder', 'foo bad builder node')

    check_id = db.checks.insert(data)

    return serialize({
        'check': check_id
    }, True)


@app.route("%s/finish" % (API_BASE), methods=['GET', 'POST'])
def finished():
    resp = api_validate(['job'])
    if resp: return resp
    (req, builder) = get_things()

    job = req['job']
    jobj = db_find('jobs', job)

    if jobj['builder'] is None:
        return api_abort('bad-builder', 'bad builder node')

    if jobj['builder'] != builder._obj['_id']:  # XXX: Fixme
        return api_abort('bad-builder', 'foo bad builder node')

    if jobj['finished']:
        return api_abort('job-wtf', 'job is already closed, dummy')

    jobj['finished'] = True
    jobj['finished_at'] = dt.datetime.now()
    db.jobs.update({"_id": jobj['_id']},
                   jobj,
                   True,
                   safe=True)

    return serialize({
        'action': 'job closed'
    }, True)


@app.route("%s/aquire" % (API_BASE), methods=['GET', 'POST'])
def aquire():
    resp = api_validate([])
    if resp: return resp
    (req, builder) = get_things()

    def _ret_job(job):
        return serialize({
            "job": job
        }, True)

    bid = builder._obj['_id']
    oldjobs = db.jobs.find({"finished": False, "builder": bid})
    if oldjobs.count() != 0:
        return _ret_job(oldjobs[0])

    jobs = db.jobs.find({
        "finished": False,
        "builder": None,
        "type": {
            "$in": builder._obj['abilities']
        }
    })
    if jobs.count() <= 0:
        return api_abort('no-jobs', 'no more jobs')

    job = jobs[0]
    job['builder'] = bid
    db.jobs.update({"_id": job['_id']},
                   job,
                   safe=True)
    return _ret_job(job)
