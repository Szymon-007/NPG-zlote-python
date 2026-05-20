
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from sqlmodel import SQLModel, select
from passlib.context import CryptContext
from models import UserLogin, UserRegister
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from JWTgen import create_access_token



#haszowanie hasla zad 3.1
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


app = FastAPI()



@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#endpoint rejestracji zad 3.2
@app.post("/reg")
def register(data: UserRegister, baza: Session = Depends(get_db)):


    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Wygenerowanie hasha z odebranego jawnego hasła
    haszowane = hash_password(data.password)

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


