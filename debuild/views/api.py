from debuild import app
from chatham.builders import Builder

import json
from flask import request

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
        return json.dumps(obj, sort_keys=True, indent=4)
    return json.dumps(obj)


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


@app.route("%s/ping" % (API_BASE), methods=['GET', 'POST'])
def ping():
    req = request.values
    if not api_validate(req):
        return api_abort('bad-sig', 'bad signature')
    builder = Builder(req['node'])
    builder.ping()
    return serialize({
        'ping': 'pung'
    }, True)


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
