from pydantic import BaseModel
from enum import Enum

# --- Zadanie 3.7: Modele dla minek ---
class MoodEnum(str, Enum):
    bardzo = "bardzo"
    srednio = "srednio"
    bardzo_nie = "bardzo_nie"

class PollSubmit(BaseModel):
    mood: MoodEnum

# --- Zadanie 3.1: Modele logowania i rejestracji ---
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str