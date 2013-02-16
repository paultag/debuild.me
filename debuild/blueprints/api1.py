#

from jinja2 import TemplateNotFound
from flask import Blueprint


api = Blueprint('apiv1', __name__, template_folder='templates')
