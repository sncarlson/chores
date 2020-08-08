"""
TODO Specifies endpoints and behavior for at least:
    Two GET requests
    One POST request
    One PATCH request
    One DELETE request
    Utilize the @app.errorhandler decorator to format error responses as JSON objects
    for at least four different status codes
"""

from flask import Blueprint

# Blueprint Configuration
controller_bp = Blueprint(
    'controller_bp', __name__,
)


@controller_bp.route('/', methods=['GET'])
def home():
    return "Hello from the controller!"
