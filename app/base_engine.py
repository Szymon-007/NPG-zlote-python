from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

base  = create_engine('sqlite:///bazalogin.db', echo=True)
session  = sessionmaker(bind=base)
base = declarative_base()


