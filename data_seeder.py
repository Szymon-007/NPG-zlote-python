from sqlmodel import Session, select
from database import engine, User, Quote, QuoteTag, ZodiacSign, hash_password

def seed_database():
    print("Rozpoczynam zasilanie bazy danych testowymi danymi...")
    
    with Session(engine) as session:
        # --- 1. DODAWANIE TESTOWEGO UŻYTKOWNIKA ---
        # Sprawdzamy, czy użytkownik już istnieje (żeby nie wywaliło błędu przy ponownym odpaleniu)
        existing_user = session.exec(select(User).where(User.email == "test@student.pl")).first()
        
        if not existing_user:
            test_user = User(
                email="test@student.pl",
                hashed_password=hash_password("haslo123"),
                zodiac_sign=ZodiacSign.wodnik
            )
            session.add(test_user)
            print("✅ Dodano testowego użytkownika: test@student.pl (hasło: haslo123)")
        else:
            print("⏩ Użytkownik test@student.pl już istnieje. Pomijam.")

        # --- 2. DODAWANIE TESTOWYCH CYTATÓW ---
        # Sprawdzamy, czy mamy już jakieś cytaty w bazie
        existing_quote = session.exec(select(Quote)).first()
        
        if not existing_quote:
            quotes_to_add = [
                # --- POCIESZAJĄCE ---
                Quote(
                    text="Nie płacz, że coś się skończyło, tylko uśmiechaj się, że ci się to przytrafiło.", 
                    author="Gabriel García Márquez", 
                    tag=QuoteTag.pocieszajacy
                ),
                Quote(
                    text="Nawet najdłuższa noc kiedyś się kończy i wschodzi słońce.", 
                    author="Victor Hugo", 
                    tag=QuoteTag.pocieszajacy
                ),

                # --- MOTYWACYJNE ---
                Quote(
                    text="Podróż tysiąca mil zaczyna się od jednego kroku.", 
                    author="Laozi", 
                    tag=QuoteTag.motywacyjny
                ),
                Quote(
                    text="Zawsze wydaje się, że coś jest niemożliwe, dopóki nie zostanie to zrobione.", 
                    author="Nelson Mandela", 
                    tag=QuoteTag.motywacyjny
                ),

                # --- ODSTRESOWUJĄCE ---
                Quote(
                    text="Ciesz się małymi rzeczami, bo pewnego dnia możesz spojrzeć wstecz i uświadomić sobie, że były to rzeczy wielkie.", 
                    author="Robert Brault", 
                    tag=QuoteTag.odstresowujacy
                ),
                Quote(
                    text="Prawdziwe szczęście polega na tym, by czerpać radość z tego, co mamy, tu i teraz.", 
                    author="Seneka", 
                    tag=QuoteTag.odstresowujacy
                ),

                # --- OGÓLNE ---
                Quote(
                    text="Dobrze widzi się tylko sercem. Najważniejsze jest niewidoczne dla oczu.", 
                    author="Antoine de Saint-Exupéry", 
                    tag=QuoteTag.ogolny
                ),
                Quote(
                    text="Prawdziwa mądrość polega na uświadomieniu sobie, jak mało w rzeczywistości wiemy.", 
                    author="Sokrates", 
                    tag=QuoteTag.ogolny
                )
            ]
            
            # session.add_all pozwala dodać całą listę obiektów za jednym zamachem
            session.add_all(quotes_to_add)
            print(f"✅ Dodano {len(quotes_to_add)} testowych cytatów do bazy.")
        else:
            print("⏩ Baza cytatów nie jest pusta. Pomijam dodawanie startowych cytatów.")

        # --- 3. ZATWIERDZENIE ZMIAN ---
        session.commit()
        print("🎉 Zakończono z sukcesem! Baza jest gotowa do testów.")

if __name__ == "__main__":
    seed_database()