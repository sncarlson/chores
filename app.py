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
