import os
import babel
from babel.dates import format_date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import SQLAlchemy
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

def setup_db(app,database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URL'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFIACATION'] = False
    db.app = app
    db.init_app(app)

'''
Modle_Owner : class is define many to many relationship
between Car_Model and Car_Owner
'''

class Model_Owner(db.Model):
    __tablename__ =  "model_owner"

    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey(models.id, ondelete="CASECADE"), nullable=False)
    onwer_id = db.Column(db.Integer, db.ForeignKey(owners.id, ondelete="CASECADE"), nullable=False)

    def __init__(self, model_id, owner_id):
        self.model_id = model_id
        self.owner_id =  owner_id

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

    id = Column(Integer, primary_key = True)
    model_name = Column(String)
    launch_date = Column(Date)
    modle_owners = db.relationship('Model_Owner', casecade="all,delete", backref="models", lazy=True)

    def __init__(self, model_name, launch_date):
        self.model_name =  model_name
        self.launch_date = launch_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.sesion.commit()
    
    def update(self):
        db.session.commit()

'''
    Car_Owner : class for table car owner's details
'''

class Car_Owner(db.Model):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True)
    owner_name = Column(String)
    purchase_date = Column(Date)
    modle_owners = db.relationship("Modle_Owner", casecade = "all,delete", lazy=True)

    def __init__(self, owner_name, purchase_date):
        self.owner_name = owner_name
        self.purchase_date = purchase_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()



