# models.py
import flask_sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float,PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import *

from main import db


class Users(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(30))
    messages = db.relationship('chatMessages', backref='users')
    
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def __repr__(self):
        return '<Username: %s>' % self.name
class chatMessages(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'))
    
    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id
        
    def __repr__(self):
        return '<Message: %s>' % self.text