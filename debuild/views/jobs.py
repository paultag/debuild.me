from debuild import app
from monomoy.core import db
from debuild.utils import db_find

from bson.objectid import ObjectId
from flask import render_template, abort


@app.route("/job/<job_id>")
def job(job_id):
    job = db_find('jobs', job_id)
    if job is None:
        abort(404)

    # XXX: Refactor all this garbage.

    return render_template('job.html', **{
        "job": job,
        "checks": db.checks.find({"job": job['_id']})
    })
