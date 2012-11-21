from debuild import app
from monomoy.core import db
from monomoy.utils import JSONEncoder
from debuild.utils import db_find
from chatham.builders import Builder

from flask import request
import json

API_BASE = '/api'
DEBUG = True


# Core verbs:
#
#  - token
#  - ping
#  - result


def serialize(obj, allok):
    obj['status'] = 'ok' if allok else 'nokay'

    if DEBUG:
        return json.dumps(obj, sort_keys=True, indent=4, cls=JSONEncoder)
    return json.dumps(obj, cls=JSONEncoder)


def api_abort(code, text):
    return serialize({
        'code': code,
        'text': text
    }, False)


def api_validate(keys):
    req = request.values
    for key in ['node', 'signature']:
        if key not in req:
            return False

    for key in keys:
        if key not in req:
            return False

    node = req['node']
    builder = Builder(node)
    return builder.validate_request(req['signature'])


@app.route('%s/token' % (API_BASE), methods=['GET', 'POST'])
def token():
    """ Unauth'd ping """
    req = request.values
    if 'node' not in req:
        return api_abort('nsp-node', 'No such param: node')

    node = req['node']
    bob = Builder(node)
    key = bob.new_token()

    return serialize({
        "token": key
    }, True)


@app.route("%s/ping" % (API_BASE), methods=['GET', 'POST'])
def ping():
    req = request.values
    if not api_validate([]):
        return api_abort('bad-sig', 'bad signature')
    builder = Builder(req['node'])
    builder.ping()
    return serialize({
        'ping': 'pung'
    }, True)


@app.route("%s/result" % (API_BASE), methods=['GET', 'POST'])
def result():
    req = request.values
    if not api_validate(['data']):
        return api_abort('bad-sig', 'bad signature')  # factor this out
    builder = Builder(req['node'])
    builder.ping()
    data = json.loads(req['data'])
    job = data['job']
    jobj = db_find('jobs', job)
    if jobj['builder'] is None:
        return api_abort('bad-builder', 'bad builder node')

    builder = Builder(jobj['builder'])
    if jobj['builder'] != builder._obj['_id']:  # XXX: Fixme
        return api_abort('bad-builder', 'foo bad builder node')

    check_id = db.checks.insert(data)

    return serialize({
        'check': check_id
    }, True)
