from fastapi import FastAPI, Depends
from sqlmodel import Session
import passlib.context
from fastapi.middleware.cors import CORSMiddleware
from app.models_mimics import UserLogin, UserRegister
from app.JWTgen import create_access_token, get_current_user
from baza_danych.database import pobierz_sesje, stworz_tabele
from app.script import calculate_ideal_tag
from baza_danych.crud import pobierz_uzytkownika_po_mailu, dodaj_uzytkownika
from baza_danych.models import QuoteTag
# Haszowanie hasla zad 3.1
pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Porty Twojego Reacta
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    stworz_tabele()


# Endpoint rejestracji zad 3.2
@app.post("/api/register")
def register(data: UserRegister, baza: Session = Depends(pobierz_sesje)):
    uzytkownik_juz_jest = pobierz_uzytkownika_po_mailu(baza, data.email)

    if uzytkownik_juz_jest:
        raise HTTPException(status_code=400, detail="Email already registered")

    haszowane = hash_password(data.password)

    # Upewnij się, że w models_mimics.py Twój UserRegister przyjmuje małe litery przesyłane z frontu
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


from datetime import date
import random
from fastapi import Depends, HTTPException
from sqlmodel import Session, select

# 1. Dokładne importy z Twoich plików
from app.models_mimics import PollSubmit
from baza_danych.models import Quote, QuoteHistory
from baza_danych.crud import (
    pobierz_uzytkownika_po_id,
    aktualizuj_date_ankiety_uzytkownika,
    pobierz_cytat_po_tagu_bez_powtorek7,
    zapisz_cytat_do_historii
)


# Założenie: funkcja calculate_ideal_tag znajduje się w odpowiednim pliku (np. app.losowanie)
# from app.losowanie import calculate_ideal_tag


# --- ENDPOINT 1: Obsługa strażnika ProtectedRoute.jsx ---
@app.get("/api/survey/status")
def sprawdz_status_ankiety(
        current_user=Depends(get_current_user),
        baza: Session = Depends(pobierz_sesje)
):
    dzisiaj = date.today()

    # Używamy Twojej funkcji pobierz_uzytkownika_po_id z crud.py
    user = pobierz_uzytkownika_po_id(baza, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie istnieje")

    wypelniono_dzisiaj = user.last_survey_date == dzisiaj
    return {"has_filled_today": wypelniono_dzisiaj}


# --- ENDPOINT 2: Zapis ankiety i losowanie (Survey.jsx) ---
@app.post("/api/survey")
def zapisz_slad_i_losuj(
    ankieta: PollSubmit,
    baza: Session = Depends(pobierz_sesje),
    aktualny_user = Depends(get_current_user)
):
    # 1. Zapisujemy datę aktywności użytkownika
    aktualizuj_date_ankiety_uzytkownika(baza, aktualny_user.id)

    # 2. Przekazujemy czyste stringi bezpośrednio do poprawionej funkcji
    wyliczony_tag_str = calculate_ideal_tag(ankieta.stress, ankieta.motivation, ankieta.humor)

    # 3. Rzutujemy wynikowy string na QuoteTag przy wywołaniu losowania z bazy
    wylosowany_cytat = pobierz_cytat_po_tagu_bez_powtorek7(
        baza,
        int(aktualny_user.id),
        QuoteTag(wyliczony_tag_str)
    )

    # 4. Drzewo fallbacków (jeśli brak unikalnego cytatu)
    if not wylosowany_cytat:
        awaryjne_cytaty = baza.exec(select(Quote).where(Quote.tag == QuoteTag(wyliczony_tag_str))).all()
        if awaryjne_cytaty:
            wylosowany_cytat = random.choice(awaryjne_cytaty)
        else:
            wszystkie_calkiem = baza.exec(select(Quote)).all()
            if wszystkie_calkiem:
                wylosowany_cytat = random.choice(wszystkie_calkiem)
            else:
                raise HTTPException(status_code=404, detail="Baza cytatów jest pusta!")

    # 5. Zapis do tabeli QuoteHistory
    zapisz_cytat_do_historii(baza, int(aktualny_user.id), int(wylosowany_cytat.id))

    return {"message": "Ankieta zapisana, cytat przygotowany."}

# --- ENDPOINT 3: Pobieranie cytatu na Dashboard (Dashboard.jsx) ---
@app.get("/api/quote/daily")
def pobierz_wylosowany_cytat_dla_dashboardu(
        baza: Session = Depends(pobierz_sesje),
        aktualny_user=Depends(get_current_user)
):
    # Pobieramy najświeższy wpis z tabeli QuoteHistory dla zalogowanego usera.
    # W crud.py nie masz funkcji do pobierania najnowszej historii ogółem, więc robimy bezpośredni select.
    najnowszy_wpis_historii = baza.exec(
        select(QuoteHistory)
        .where(QuoteHistory.user_id == aktualny_user.id)
        .order_by(QuoteHistory.id.desc())
    ).first()

    if not najnowszy_wpis_historii:
        raise HTTPException(status_code=404, detail="Nie znaleziono wylosowanego cytatu na dziś.")

    # Wyciągamy zawartość cytatu na podstawie zapisanego przed chwilą quote_id
    cytat = baza.get(Quote, najnowszy_wpis_historii.quote_id)
    if not cytat:
        raise HTTPException(status_code=404, detail="Cytat nie istnieje w bazie.")


    return {
        "text": cytat.text,
        "author": cytat.author,
        "category": cytat.tag
    }