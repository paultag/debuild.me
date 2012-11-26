# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

import json
from flask import Flask

monomoy = json.load(open('monomoy.json', 'r'))  # XXX: Fixme
app = Flask(__name__)


from debuild.utils import load_modules_from_json
load_modules_from_json('modules.json')  # XXX: Fixme
