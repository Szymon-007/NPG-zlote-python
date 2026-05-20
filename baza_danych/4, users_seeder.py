from sqlmodel import Session, select
from database import engine
from models import User, ZodiacSign
 
 
USERS = [
    {"email": "anna.kowalska@gmail.com",   "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.baran},
    {"email": "piotr.nowak@gmail.com",     "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.byk},
    {"email": "karolina.wis@gmail.com",    "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.bliznieta},
    {"email": "marek.lis@gmail.com",       "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.rak},
    {"email": "zofia.maj@gmail.com",       "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.lew},
    {"email": "tomasz.wrobel@gmail.com",   "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.panna},
    {"email": "ewa.kaminska@gmail.com",    "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.waga},
    {"email": "lukasz.zak@gmail.com",      "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.skorpion},
    {"email": "natalia.bak@gmail.com",     "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.strzelec},
    {"email": "michal.krol@gmail.com",     "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.koziorozec},
    {"email": "julia.szymanska@gmail.com", "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.wodnik},
    {"email": "adam.pawlak@gmail.com",     "hashed_password": "haslo123", "zodiac_sign": ZodiacSign.ryby},
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