from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel, create_engine
from passlib.context import CryptContext

# --- 1. KONFIGURACJA HASZOWANIA ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# --- 2. ENUMY (Opcje wyboru) ---
class ZodiacSign(str, Enum):
    baran = "baran"
    byk = "byk"
    bliznieta = "bliznieta"
    rak = "rak"
    lew = "lew"
    panna = "panna"
    waga = "waga"
    skorpion = "skorpion"
    strzelec = "strzelec"
    koziorozec = "koziorozec"
    wodnik = "wodnik"
    ryby = "ryby"

class QuoteTag(str, Enum):
    pocieszajacy = "pocieszajacy"
    motywacyjny = "motywacyjny"
    odstresowujacy = "odstresowujacy"
    ogolny = "ogolny"


# --- 3. MODELE BAZODANOWE (Tabele) ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    zodiac_sign: ZodiacSign = Field(nullable=False)

class Quote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(nullable=False)
    author: Optional[str] = Field(default="Anonim")
    tag: QuoteTag = Field(nullable=False)


# --- 4. KONFIGURACJA BAZY DANYCH ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Pełna struktura bazy (User oraz Quote) jest gotowa!")