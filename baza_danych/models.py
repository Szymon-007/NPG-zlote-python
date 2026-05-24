from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, date
from enum import Enum

class ZodiacSign(str, Enum):
    Baran = "Baran"
    Byk = "Byk"
    Bliznieta = "Bliznieta"
    Rak = "Rak"
    Lew = "Lew"
    Panna = "Panna"
    Waga = "Waga"
    Skorpion = "Skorpion"
    Strzelec = "Strzelec"
    Koziorozec = "Koziorozec"
    Wodnik = "Wodnik"
    Ryby = "Ryby"

class QuoteTag(str, Enum):
    pocieszajacy = "pocieszajacy"
    motywacyjny = "motywacyjny"
    odstresowujacy = "odstresowujacy"
    ogolny = "ogolny"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    zodiac_sign: ZodiacSign = Field(nullable=False)
    last_survey_date: Optional[date] = Field(default=None) 


class Quote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(nullable=False)
    author: Optional[str] = Field(default="Anonim")
    tag: QuoteTag = Field(nullable=False)


class QuoteHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    quote_id: int = Field(foreign_key="quote.id", nullable=False)
    received_at: datetime = Field(default_factory=datetime.now, nullable=False)