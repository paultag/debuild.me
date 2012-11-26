from debuild import app
from monomoy.core import db
from bson.objectid import ObjectId
from debuild.utils import db_find

from flask import render_template, abort


@app.route("/user/<user_id>")
def user(user_id):
    user = db_find('users', user_id)
    if user is None:
        abort(404)

    return render_template('user.html', **{
        "user": user,
        "packages": db.packages.find({"user": user['_id']}),
        "builders": db.builders.find({"owner": user['_id']})
    })
