"""

TODO Project includes a custom @requires_auth decorator that:
    get the Authorization header from the request
    Decode and verify the JWT using the Auth0 secret
    take an argument to describe the action
        i.e. @require_auth(‘create:drink’)

    TODO raise an error if:
        the token is expired
        the claims are invalid
        the token is invalid
        the JWT doesn't contain the proper action

TODO Project includes at least two different roles that have distinct permissions for actions.
 These roles and permissions are clearly defined in the project README. Students can reference the
 Casting Agency Specs in the Specifications section of this rubric as an example.
"""

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('setup.py')

    from model.models import db
    db.app = app
    db.init_app(app)
    db.create_all()

    with app.app_context():
        from controller import controller

        app.register_blueprint(controller.controller_bp)

    return app
