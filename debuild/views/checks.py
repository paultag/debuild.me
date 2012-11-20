from debuild import app
from monomoy.core import db
from bson.objectid import ObjectId
from collections import defaultdict

from flask import render_template, abort


@app.route("/check/<check_id>")
def check(check_id):
    check = db.checks.find_one({"_id": check_id})
    if check is None:
        check = db.checks.find_one({"_id": ObjectId(check_id)})

    if check is None:
        abort(404)

    tags = defaultdict(lambda: defaultdict(int))
    for block in check['data']:
        obj = check['data'][block]
        for ch in obj:
            tags[block][ch['tag']] += 1

    return render_template('check.html', **{
        "check": check,
        "tags": tags
    })
