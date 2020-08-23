# TODO Use of correct data types for fields
# TODO Use of primary and optional foreign key ids

# TODO Does not use raw SQL or only where there are
#  not SQLAlchemy equivalent expressions
# TODO Correctly formats SQLAlchemy to define models
# TODO Creates methods to serialize model data and
#  methods to simplify API behavior
#  such as insert, update and delete.

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def setup_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()


class Chore(db.Model):
    __tablename__ = 'Chore'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('Area.id'), nullable=False)
    assigned_chores = relationship('AssignedChore', backref='chore',
                                   lazy=True, cascade="all, delete")

    def __init__(self, description, cost, area_id):
        self.description = description
        self.cost = cost
        self.area_id = area_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'description': self.description,
            'cost': self.cost,
            'area_id': self.area_id
        }


class Area(db.Model):
    __tablename__ = 'Area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    chores = relationship('Chore', backref='area',
                          lazy=True, cascade="all, delete")

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Worker(db.Model):
    __tablename__ = 'Worker'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    assigned_chores = relationship('AssignedChore',
                                   backref='worker', lazy=True)

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class AssignedChore(db.Model):
    __tablename__ = 'AssignedChore'
    id = db.Column(db.Integer, primary_key=True)
    chore_id = db.Column(db.Integer, db.ForeignKey('Chore.id'), nullable=False)
    worker_id = db.Column(db.Integer,
                          db.ForeignKey('Worker.id'), nullable=False)
    duration = db.Column(db.String(120), nullable=False)
    frequency = db.Column(db.String(120), nullable=False)

    def __init__(self, chore_id, worker_id, duration, frequency):
        self.chore_id = chore_id
        self.worker_id = worker_id
        self.duration = duration
        self.frequency = frequency

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'chore_id': self.chore_id,
            'worker_id': self.worker_id,
            'duration': self.duration,
            'frequency': self.frequency
        }
