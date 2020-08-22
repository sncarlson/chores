import os

from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('setup.py')

    from model.models import db
    db.app = app
    db.init_app(app)
    db.create_all()
    CORS(app)

    with app.app_context():
        from controller import controller
        app.register_blueprint(controller.controller_bp)

    return app


app = create_app()
