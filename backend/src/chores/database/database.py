# TODO Implement Database here
from flask import current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

print(current_app.config['SQLALCHEMY_DATABASE_URI'])
