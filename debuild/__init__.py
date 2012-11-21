# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

import json
from flask import Flask

from monomoy.utils import JSONEncoder
from debuild.utils import load_modules_from_json

app = Flask(__name__)
API_BASE = '/api'

load_modules_from_json('modules.json')  # XXX: Fixme


def serialize(obj):
    return json.dumps(obj, cls=JSONEncoder)
