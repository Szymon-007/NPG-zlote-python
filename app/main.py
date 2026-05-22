from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
import passlib.context
from fastapi.middleware.cors import CORSMiddleware
from app.models_mimics import UserLogin, UserRegister
from app.JWTgen import create_access_token, get_current_user
from baza_danych.database import pobierz_sesje, stworz_tabele

# Importujemy funkcje z Twojego pliku crud
from baza_danych.crud import pobierz_uzytkownika_po_mailu, dodaj_uzytkownika

# Haszowanie hasla zad 3.1
pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Porty Twojego Reacta
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def on_startup():
    stworz_tabele()

# Endpoint rejestracji zad 3.2
# Zmieniona ścieżka na /api/register
@app.post("/api/register")
def register(data: UserRegister, baza: Session = Depends(pobierz_sesje)):
    uzytkownik_juz_jest = pobierz_uzytkownika_po_mailu(baza, data.email)

    if uzytkownik_juz_jest:
        raise HTTPException(status_code=400, detail="Email already registered")

    haszowane = hash_password(data.password)

    # TUTAJ ZMIANA: z data.zodiac na data.zodiac_sign
    nowy_user = dodaj_uzytkownika(baza, data.email, haszowane, data.zodiac_sign)

    dane = {"sub": str(nowy_user.id), "email": str(nowy_user.email)}
    token = create_access_token(data=dane)

    return {
        "message": "Registered successfully",
        "access_token": token,
        "token_type": "bearer"
    }



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
    return {"has_filled_today": False}