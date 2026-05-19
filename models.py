from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from enum import Enum
from datetime import date

# --- Zadanie 3.7: Modele dla minek ---
class MoodEnum(str, Enum):
    bardzo = "bardzo"
    srednio = "srednio"
    bardzo_nie = "bardzo_nie"

class Poll(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_date: date = Field(default_factory=date.today)
    stress: MoodEnum
    motivation: MoodEnum
    mood: MoodEnum
    user_id: int | None = Field(default=None, foreign_key="user.id")

class PollSubmit(BaseModel):
    stress: MoodEnum
    motivation: MoodEnum
    mood: MoodEnum

# --- Zadanie 3.1: Modele logowania i rejestracji ---
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str