from typing import Optional

from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, create_engine
from passlib.context import CryptContext



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    zodiac_sign: Optional[str] = Field(default=None)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)
session = sessionmaker(bind=engine)


def get_db():
    sesja = session()
    try:
        yield sesja
    finally:
        sesja.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
