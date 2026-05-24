from sqlmodel import Session, select
from baza_danych.database import engine
from baza_danych.models import User, Quote, QuoteHistory
from datetime import datetime, timedelta
import random


# Ile wpisów historii wygenerować na użytkownika
# Przy 8 cytatach dajemy 3, żeby zostały cytaty "nowe" do testów
WPISY_NA_USERA = 3

# Zakres dat wstecz (w dniach) z jakiego losowane są daty otrzymania cytatu
ZAKRES_DNI = 30


def seed_quote_history():
    print("Dodaję historię cytatów...")

    with Session(engine) as session:
        uzytkownicy = session.exec(select(User)).all()
        cytaty = session.exec(select(Quote)).all()

        if not uzytkownicy:
            print("Brak użytkowników — najpierw uruchom seed_users.py")
            return
        if not cytaty:
            print("Brak cytatów — najpierw uruchom seed_quotes.py")
            return

        ma_history = session.exec(select(QuoteHistory)).first()
        if ma_history:
            print("Historia cytatów już istnieje. Pomijam.")
            return

        teraz = datetime.now()
        wpisy = []

        for user in uzytkownicy:
            wybrane = random.sample(cytaty, min(WPISY_NA_USERA, len(cytaty)))

            for i, cytat in enumerate(wybrane):
                # Każdy wpis w innym dniu, żeby nie było duplikatów tego samego dnia
                delta = timedelta(days=random.randint(0, ZAKRES_DNI), hours=random.randint(0, 23))
                data_otrzymania = teraz - delta

                wpis = QuoteHistory(
                    user_id=user.id,
                    quote_id=cytat.id,
                    received_at=data_otrzymania,
                )
                wpisy.append(wpis)

        session.add_all(wpisy)
        session.commit()

    print(f"Dodano {len(wpisy)} wpisów historii dla {len(uzytkownicy)} użytkowników.")


if __name__ == "__main__":
    seed_quote_history()