from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')

    from .database.database import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .controller import controller

        app.register_blueprint(controller.controller_bp)

    return app
