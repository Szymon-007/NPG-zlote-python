from sqlmodel import Session, select
import random
from datetime import datetime, timedelta, time
from typing import Optional
from baza_danych.models import User, ZodiacSign, Quote, QuoteHistory, QuoteTag


def zapisz_cytat_do_historii(sesja: Session, user_id: int, quote_id: int):
    nowy_wpis = QuoteHistory(user_id=user_id, quote_id=quote_id)
    sesja.add(nowy_wpis)
    sesja.commit()


def pobierz_uzytkownika_po_mailu(sesja: Session, email: str):
    zapytanie = select(User).where(User.email == email)
    return sesja.exec(zapytanie).first()

def dodaj_uzytkownika(
        sesja: Session,
        email: str,
        hash_haslo: str,
        zodiak: ZodiacSign = None):
    
    nowy_user = User(
        email=email,
        hashed_password=hash_haslo,
        zodiac_sign=zodiak         
    )
    
    sesja.add(nowy_user)
    sesja.commit()
    sesja.refresh(nowy_user)
    return nowy_user

    
def pobierz_cytat_po_tagu_bez_powtorek7(sesja: Session, user_id: int, tag: QuoteTag) -> Optional[Quote]:

    tydzien_temu = datetime.now() - timedelta(days=7)


    history_stmt = select(QuoteHistory.quote_id).where(
        QuoteHistory.user_id == user_id,
        QuoteHistory.received_at >= tydzien_temu
    )
    recent_quote_ids = sesja.exec(history_stmt).all()

    stmt = select(Quote).where(Quote.tag == tag)

    if recent_quote_ids:
        stmt = stmt.where(Quote.id.notin_(recent_quote_ids))

    available_quotes = sesja.exec(stmt).all()

    if not available_quotes:
        return None
        
    return random.choice(available_quotes)


def pobierz_wczorajszy_cytat(sesja: Session, user_id: int) -> Optional[Quote]:
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    start_of_yesterday = datetime.combine(yesterday, time.min)
    start_of_today = datetime.combine(today, time.min)

    statement = (
        select(Quote)
        .join(QuoteHistory)
        .where(QuoteHistory.user_id == user_id)
        .where(QuoteHistory.received_at >= start_of_yesterday)
        .where(QuoteHistory.received_at < start_of_today)
    )

    return sesja.exec(statement).first()