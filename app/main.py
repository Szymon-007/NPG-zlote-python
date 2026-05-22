from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
import passlib.context

from app.models_mimics import UserLogin, UserRegister
from app.JWTgen import create_access_token, get_current_user
from app.database import pobierz_sesje

# Importujemy funkcje z Twojego pliku crud
from app.crud import pobierz_uzytkownika_po_mailu, dodaj_uzytkownika

# Haszowanie hasla zad 3.1
pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


app = FastAPI()


# Endpoint rejestracji zad 3.2
# Zmieniona ścieżka na /api/register
@app.post("/api/register")
def register(data: UserRegister, baza: Session = Depends(pobierz_sesje)):
    uzytkownik_juz_jest = pobierz_uzytkownika_po_mailu(baza, data.email)

    if uzytkownik_juz_jest:
        raise HTTPException(status_code=400, detail="Email already registered")

    haszowane = hash_password(data.password)
    nowy_user = dodaj_uzytkownika(baza, data.email, haszowane, data.zodiac)

    # Dodano generowanie tokena po rejestracji (zgodnie z instrukcją z README)
    dane = {"sub": str(nowy_user.id), "email": str(nowy_user.email)}
    token = create_access_token(data=dane)

    return {
        "message": "Registered successfully",
        "access_token": token,  # <--- Frontend zapisze to w localStorage
        "token_type": "bearer"
    }


# Logowanie zostaje takie, jakie było (tylko upewnij się, że jest /api/login)
@app.post("/api/login")
def login(data: UserLogin, baza: Session = Depends(pobierz_sesje)):
    user = pobierz_uzytkownika_po_mailu(baza, data.email)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    dane = {"sub": str(user.id), "email": str(user.email)}
    token = create_access_token(data=dane)

    return {"access_token": token, "token_type": "bearer"}


# Endpoint statusu
@app.get("/status-uzytkownika")
def sprawdz_status_ankiety(current_user=Depends(get_current_user), baza: Session = Depends(pobierz_sesje)):
    # Zmieniony klucz JSON-a zgodnie z zaleceniem frontendu
    return {"has_filled_today": False}