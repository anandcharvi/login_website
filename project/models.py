from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    book_name = db.Column(db.String(100), unique=True)
    Inventory = db.Column(db.Integer)
    
class books_record(db.Model):
    ref_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    status = db.Column(db.String(10))
    issue_date = db.Column(db.DateTime(timezone=True), default=func.now())
    return_date = issue_date + 30
    
    


