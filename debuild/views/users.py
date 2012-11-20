from debuild import app
from monomoy.core import db
from bson.objectid import ObjectId

from flask import render_template, abort


@app.route("/user/<user_id>")
def user(user_id):
    user = db.users.find_one({"_id": user_id})
    if user is None:
        user = db.users.find_one({"_id": ObjectId(user_id)})

    if user is None:
        abort(404)

    return render_template('user.html', **{
        "user": user,
        "packages": db.packages.find({"user": user['_id']})
    })
