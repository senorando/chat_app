# models.py
import flask_sqlalchemy
from main import db


class chatUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(120))
    
    def __init__(self, a):
        self.message = a
        
    def __repr__(self):
        return '<User: %s>' % self.message

