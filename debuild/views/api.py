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
    # pull requesting node
    # pull last token
    # pull secret key
    # check signature matches (token + key)
    # abort or pass
    pass


@app.route('%s/token' % (API_BASE))
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
