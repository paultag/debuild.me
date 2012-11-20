from debuild import app
from monomoy.core import db
from bson.objectid import ObjectId

from flask import render_template, abort


@app.route("/job/<job_id>")
def job(job_id):
    job = db.jobs.find_one({"_id": job_id})
    if job is None:
        job = db.jobs.find_one({"_id": ObjectId(job_id)})
    if job is None:
        abort(404)

    # XXX: Refactor all this garbage.

    return render_template('job.html', **{
        "job": job,
        "checks": db.checks.find({"job": job['_id']})
    })
