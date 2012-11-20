import json
import importlib


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
