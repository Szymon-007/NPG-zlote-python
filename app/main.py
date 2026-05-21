
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.functions import user
from passlib.context import CryptContext
from baza_danych.models import UserLogin, UserRegister
from JWTgen import create_access_token
from database import pobierz_sesje
from crud import *



#haszowanie hasla zad 3.1
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


app = FastAPI()
sesja = pobierz_sesje()
@app.post("/reg")
def register(data: UserRegister, baza: Session = Depends(pobierz_sesje)):
    uzytkownik_juz_jest  = pobierz_uzytkownika_po_mailu(baza, data.email)
    if uzytkownik_juz_jest():
        raise HTTPException(status_code=400, detail="Email already registered")

    haszowane = hash_password(data.password)
    dodaj_uzytkownika(baza, data.email, haszowane)
    return {"message": "Registered successfully", "user_id": data.id}

#endpoint logowania zad 3.3

#przydiela acces token
@app.post("/log")
def login(data: UserLogin, baza: Session = Depends(get_db)):

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    dane = {"sub": str(user.id), "email": str(user.email)}
    token = create_access_token(data = dane)
    return {"access_token": token, "token_type": "bearer"}

    return {"message": "Logged in successfully", "user_id": user.id}


