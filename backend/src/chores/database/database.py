# TODO Implement Database here
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

db = SQLAlchemy()
migrate = Migrate()

