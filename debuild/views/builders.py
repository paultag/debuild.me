from debuild import app
from chatham.builders import Builder

from flask import render_template, abort


@app.route("/builder/<builder_id>")
def builder(builder_id):
    builder = Builder(builder_id)

    return render_template('builder.html', **{
        "builder": builder
    })
