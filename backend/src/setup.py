import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

SQLALCHEMY_DATABASE_URI = 'postgres://test:test@hive:5432/test'
SQLALCHEMY_TRACK_MODIFICATION = False