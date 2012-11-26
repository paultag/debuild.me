import json
import importlib
from bson.objectid import ObjectId

from monomoy.core import db


def load_module(obj_path):
    module = obj_path
    mod = importlib.import_module(module)
    return mod


def load_modules(obj):
    for module in obj:
        load_module(module)


def load_modules_from_json(fn):
    obj = json.load(open(fn, 'r'))
    load_modules(obj)


def db_find(typ, eyedee):
    obj = getattr(db, typ).find_one({"_id": eyedee})
    if obj is None:
        obj = getattr(db, typ).find_one({"_id": ObjectId(eyedee)})
    return obj
