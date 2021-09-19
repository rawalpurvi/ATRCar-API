import os
import babel
from babel.dates import format_date
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    create_engine
)

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds flask app to the sqlalchemy database
'''


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


'''
Model_Owner : class is define many to many relationship
between Car_Model and Car_Owner
'''


class Model_Owner(db.Model):
    __tablename__ = "model_owner"

    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey(
        'models.id', ondelete="CASCADE"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'owners.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, model_id, owner_id):
        self.model_id = model_id
        self.owner_id = owner_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''
Car_Model : class for table car model details
'''


class Car_Model(db.Model):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    launch_date = Column(Date)
    model_owners = db.relationship(
        'Model_Owner', cascade="all, delete", backref='models', lazy=True)

    def __init__(self, model_name, launch_date):
        self.model_name = model_name
        self.launch_date = launch_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):

        # set release date in format
        formatDate = "EEEE, dd MMMM YYYY"
        format_launch_date = babel.dates.format_date(
            self.launch_date, formatDate)

        return {
            'id': self.id,
            'model_name': self.model_name,
            'launch_date': format_launch_date
        }


'''
 Car_Owner : class for table car owner's details
'''


class Car_Owner(db.Model):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True)
    owner_name = Column(String)
    address = Column(String)
    model_owners = db.relationship(
        "Model_Owner", cascade="all, delete", backref='owners', lazy=True)

    def __init__(self, owner_name, address):
        self.owner_name = owner_name
        self.address = address

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        owner_car_names = []
        owner_cars = db.session.query(Car_Model.model_name).filter(
            Model_Owner.owner_id == self.id,
            Model_Owner.model_id == Car_Model.id).order_by(Car_Model.id).all()
        owner_car_names = [car.model_name for car in owner_cars]

        return {
            'id': self.id,
            'owner_name': self.owner_name,
            'address': self.address,
            'owner_car_names': owner_car_names
        }
