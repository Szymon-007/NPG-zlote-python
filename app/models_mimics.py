from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from enum import Enum
from datetime import date
from baza_danych.models import *

# --- Zadanie 3.7: Modele dla minek ---
class MoodEnum(str, Enum):
    bardzo = "bardzo"
    srednio = "srednio"
    bardzo_nie = "bardzo_nie"


class Poll(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_date: date = Field(default_factory=date.today)
    stress: str
    motivation: str
    humor: MoodEnum
    user_id: int | None = Field(default=None, foreign_key="user.id")


class PollSubmit(BaseModel):
    # Model używany do odbierania danych z frontendu
    stress: str
    motivation: str
    humor: str


class UserRegister(BaseModel):
    password: str
    email: str
    name: str
    # Zmieniono nazwę z 'zodiac' na 'zodiac_sign'
    zodiac_sign: ZodiacSign


class UserLogin(BaseModel):
    email: str
    password: str