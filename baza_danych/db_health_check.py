from sqlmodel import Session, select
from baza_danych.database import engine
from baza_danych.models import User, Quote, QuoteHistory

def check_database_consistency():
    print("ROZPOCZYNAM KONTROLĘ SPÓJNOŚCI I ZAWARTOŚCI BAZY DANYCH...\n")
    
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        quotes = session.exec(select(Quote)).all()
        history_entries = session.exec(select(QuoteHistory)).all()
        
        print("STATUS ZAWARTOŚCI:")
        print(f"  -> Użytkownicy: {len(users)}")
        print(f"  -> Cytaty: {len(quotes)}")
        print(f"  -> Wpisy w historii: {len(history_entries)}\n")
        
        print("KONTROLA SPÓJNOŚCI RELACJI:")
        user_ids = {u.id for u in users}
        quote_ids = {q.id for q in quotes}
        
        bledy_spojnosci = 0
        
        for entry in history_entries:
            if entry.user_id not in user_ids:
                print(f"  [BŁĄD] Wpis historii ID:{entry.id} wskazuje na nieistniejącego użytkownika (user_id:{entry.user_id})!")
                bledy_spojnosci += 1
                
            if entry.quote_id not in quote_ids:
                print(f"  [BŁĄD] Wpis historii ID:{entry.id} wskazuje na nieistniejący cytat (quote_id:{entry.quote_id})!")
                bledy_spojnosci += 1
                
        if bledy_spojnosci == 0:
            print("  Baza jest w 100% spójna. Brak osieroconych rekordów w historii.")
        else:
            print(f"  Znaleziono błędy spójności: {bledy_spojnosci}. Wymagana interwencja!")

if __name__ == "__main__":
    check_database_consistency()