import os
import smtplib
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlmodel import Session, select
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "baza_danych"))

from baza_danych.models import User
from baza_danych.database import engine
from baza_danych.crud import pobierz_wczorajszy_cytat
from baza_danych.database import stworz_tabele
from baza_danych.users_seeder import seed_users
from baza_danych.quotes_seeder import seed_quotes
from baza_danych.quotes_history_seeder import seed_quote_history

sciezka_do_bazy = 'database.db'
from datetime import date, timedelta

# Odejmujemy 1 dzień od realnej daty

def bazki():
    if not os.path.exists(sciezka_do_bazy):
        stworz_tabele()
        ##seed_users()
        seed_quotes()
        seed_quote_history()
    else:
        print(f"baza juz jest")


class EmailSender:
    def __init__(self):
        load_dotenv()
        self.nadawca = os.getenv("NADAWCA")
        self.haslo = os.getenv("HASLO_APLIKACJI")

        if not self.nadawca or not self.haslo:
            raise ValueError("Brak danych logowania! Sprawdź plik .env.")

        self.serwer = smtplib.SMTP("smtp.gmail.com", 587)
        self.serwer.starttls()
        self.serwer.login(self.nadawca, self.haslo)

    def wyslij_html_email(self, odbiorca: str, cytat: str, autor: str, link: str):
        sciezka_szablonu = os.path.join(os.path.dirname(__file__), "email_template.html")
        with open(sciezka_szablonu, "r", encoding="utf-8") as plik:
            surowy_szablon = plik.read()

        szablon = Template(surowy_szablon)
        gotowy_html = szablon.substitute(cytat=cytat, autor=autor, link=link)

        wiadomosc = MIMEMultipart("alternative")
        wiadomosc["Subject"] = "Twoja codzienna dawka inspiracji"
        wiadomosc["From"] = self.nadawca
        wiadomosc["To"] = odbiorca

        czesc_html = MIMEText(gotowy_html, "html", "utf-8")
        wiadomosc.attach(czesc_html)
        self.serwer.sendmail(self.nadawca, odbiorca, wiadomosc.as_string())

        print(f"Pomyślnie wysłano e-mail do: {odbiorca}")

    def zamknij(self):
        self.serwer.quit()


# --- Główna funkcja orkiestrująca ---

def proces_masowej_wysylki():
    print("Rozpoczynam poranną wysyłkę e-maili...")

    with Session(engine) as sesja:
        wszyscy_uzytkownicy = sesja.exec(select(User)).all()

    if not wszyscy_uzytkownicy:
        print("Baza jest pusta. Przerywam operację.")
        return

    bazowy_link = "http://localhost:5173/login"

    wyslano = 0

    try:
        mailer = EmailSender()

        with Session(engine) as sesja:
            for uzytkownik in wszyscy_uzytkownicy:

                wczorajszy_cytat = pobierz_wczorajszy_cytat(sesja, uzytkownik.id)

                if wczorajszy_cytat is None:
                    print(f"Brak wczorajszego cytatu dla: {uzytkownik.email} — wysyłam informację.")
                    tekst_cytatu = "Wczoraj nie otrzymałeś żadnego cytatu."
                    autor = ""
                    link = bazowy_link
                else:
                    tekst_cytatu = wczorajszy_cytat.text
                    autor = wczorajszy_cytat.author or "Anonim"
                    link = f"{bazowy_link}/{wczorajszy_cytat.id}"

                mailer.wyslij_html_email(
                    odbiorca=uzytkownik.email,
                    cytat=tekst_cytatu,
                    autor=autor,
                    link=link,
                )
                wyslano += 1
                if wyslano >=40:
                    break

        print(f"Zakończono wysyłkę: {wyslano} e-maili wysłanych.")

    except Exception as e:
        print(f"Wystąpił błąd podczas wysyłki: {e}")

    finally:
        if "mailer" in locals():
            mailer.zamknij()


# --- Zegar systemowy ---

# if __name__ == "__main__":
#     zegar = BlockingScheduler()
#     zegar.add_job(proces_masowej_wysylki, "cron", hour=8, minute=0)

#     print("Skrypt worker'a uruchomiony. Oczekiwanie na godzinę 08:00...")
#     zegar.start()

if __name__ == "__main__":
    bazki()
    proces_masowej_wysylki()