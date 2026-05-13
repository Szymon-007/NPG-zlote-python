
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, func
from base_engine import base


class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
class Quote(base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    tags = Column(String)
class History(base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    quote_id = Column(Integer, ForeignKey('quote.id'))
    send_at = Column(DateTime, server_default=func.now())



