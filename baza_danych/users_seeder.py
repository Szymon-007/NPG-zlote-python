from sqlmodel import Session, select
from baza_danych.database import engine
from baza_danych.models import User, ZodiacSign
 
 
USERS = [
    {"email": "anna.kowalska@gmail.com",   "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Baran},
    {"email": "piotr.nowak@gmail.com",     "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Byk},
    {"email": "karolina.wis@gmail.com",    "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Bliznieta},
    {"email": "marek.lis@gmail.com",       "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Rak},
    {"email": "zofia.maj@gmail.com",       "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Lew},
    {"email": "tomasz.wrobel@gmail.com",   "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Panna},
    {"email": "ewa.kaminska@gmail.com",    "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Waga},
    {"email": "lukasz.zak@gmail.com",      "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Skorpion},
    {"email": "natalia.bak@gmail.com",     "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Strzelec},
    {"email": "michal.krol@gmail.com",     "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Koziorozec},
    {"email": "julia.szymanska@gmail.com", "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Wodnik},
    {"email": "adam.pawlak@gmail.com",     "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.Ryby},
]
 
 
def seed_users():
    print("Dodaję użytkowników...")
 
    with Session(engine) as session:
        dodano = 0
 
        for data in USERS:
            istnieje = session.exec(
                select(User).where(User.email == data["email"])
            ).first()
 
            if not istnieje:
                user = User(**data)
                session.add(user)
                dodano += 1
            else:
                print(f"Pomijam (już istnieje): {data['email']}")
 
        session.commit()
 
    print(f"Dodano {dodano} nowych użytkowników.")
 
 
if __name__ == "__main__":
    seed_users()