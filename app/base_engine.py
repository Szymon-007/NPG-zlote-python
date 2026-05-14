from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine  = create_engine('sqlite:///bazalogin.db', echo=True)
session  = sessionmaker(bind=engine, autoflush=False, autocommit=False)
base = declarative_base()
def get_db():
    bazadanych = session()
    try:
        yield bazadanych
    finally:
        bazadanych.close()
