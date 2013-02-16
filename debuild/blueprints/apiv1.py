#

from flask import Blueprint


api = Blueprint('apiv1', __name__, template_folder='templates')


@api.route("/")
def index():
    return "Hello, World."
