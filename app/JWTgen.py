from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

# Import sesji oraz funkcji crud
from baza_danych.database import pobierz_sesje
from baza_danych.crud import pobierz_uzytkownika_po_mailu

# DODANO: Import modelu User.
# Zmień tę ścieżkę, jeśli plik z modelem User nazywa się inaczej (np. from models import User)
from baza_danych.models import User

SECRET_KEY = "twoj_bardzo_tajny_i_dlugi_klucz_do_podpisywania_tokenow"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 wskazuje na poprawny endpoint z ukośnikiem
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), baza: Session = Depends(pobierz_sesje)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_email: str = payload.get("email")
        if user_email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = pobierz_uzytkownika_po_mailu(baza, user_email)

    if user is None:
        raise credentials_exception

    return user