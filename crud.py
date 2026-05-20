from sqlmodel import Session, select
import random
from datetime import datetime, timedelta, time
from typing import Optional
from models import User, ZodiacSign, Quote, QuoteHistory, QuoteTag

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

    # 1. Wyliczamy dokładny czas sprzed 7 dni
    tydzien_temu = datetime.now() - timedelta(days=7)


    history_stmt = select(QuoteHistory.quote_id).where(
        QuoteHistory.user_id == user_id,
        QuoteHistory.received_at >= tydzien_temu
    )
    # Wyciągamy same identyfikatory do listy, np. [2, 5, 12]
    recent_quote_ids = sesja.exec(history_stmt).all()

    # 3. Budujemy GŁÓWNE zapytanie: "Daj mi cytaty z tym tagiem..."
    stmt = select(Quote).where(Quote.tag == tag)

    # 4. Jeśli użytkownik dostał już jakieś cytaty, dodajemy warunek wykluczający
    if recent_quote_ids:
        # Quote.id.notin_() to polecenie SQL: "gdzie ID nie znajduje się na liście..."
        stmt = stmt.where(Quote.id.notin_(recent_quote_ids))

    # 5. Wykonujemy zapytanie - teraz mamy tylko "świeże" cytaty!
    available_quotes = sesja.exec(stmt).all()

    # 6. Jeśli lista jest pusta (użytkownik wyczerpał pulę w tej kategorii), zwracamy None
    if not available_quotes:
        return None
        
    # 7. Zwracamy jeden losowy cytat z dostępnej puli
    return random.choice(available_quotes)


def pobierz_wczorajszy_cytat(sesja: Session, user_id: int) -> Optional[Quote]:
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    # 2. Tworzymy ramy czasowe: od wczoraj 00:00:00 do dzisiaj 00:00:00
    start_of_yesterday = datetime.combine(yesterday, time.min)
    start_of_today = datetime.combine(today, time.min)

    # 3. Tworzymy zapytanie korzystając z potęgi złączeń (JOIN)
    statement = (
        select(Quote)
        .join(QuoteHistory) # Łączymy tabelę cytatów z tabelą historii
        .where(QuoteHistory.user_id == user_id)
        .where(QuoteHistory.received_at >= start_of_yesterday)
        .where(QuoteHistory.received_at < start_of_today)
    )

    return sesja.exec(statement).first()