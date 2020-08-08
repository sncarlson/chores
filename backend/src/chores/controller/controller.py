# TODO Implement end points here
from flask import Blueprint, render_template
from flask import current_app as app


# Blueprint Configuration
controller_bp = Blueprint(
    'controller_bp', __name__,
)


@controller_bp.route('/', methods=['GET'])
def home():
    return "Hello from the controller!"
