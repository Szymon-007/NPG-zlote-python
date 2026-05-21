Folder składa się z trzech plików inicjalizujących bazę danych a w niej trzy tabele:
    1. tabela użytkowników (User)
    2. tabela cytatów (Quote)
    3. historia cytatów (QuoteHistory)

Za inicjalizacje odpowiadaja dwa pliki:
"database.py" - wywołanie tego pliku pliku powoduje stworzenie bazy danych lokalnie 
"models.py" - plik podrzędny opisujący struktury tabel; w linijkach 26-45 opisane są nazwy i kolumny poszczególnych tabel

plik "crud.py" zaawiera zestaw funkcji potrzebnych do wykonywania operacji na bazie danych; są to kolejno:
- zapisz_cytat_do_historii(sesja, user_id, quote_id): Zapisuje w bazie fakt, że dany użytkownik otrzymał konkretny cytat (dodaje wpis z obecną datą).
- pobierz_uzytkownika_po_mailu(sesja, email): Wyszukuje i zwraca obiekt użytkownika na podstawie jego adresu email.
- dodaj_uzytkownika(sesja, email, hash_haslo, zodiak): Tworzy nowego użytkownika w tabeli "User" i od razu go zwraca.
- pobierz_cytat_po_tagu_bez_powtorek7(sesja, user_id, tag): Główna funkcja do losowania cytatu. Filtruje cytaty po wybranym tagu i upewnia się, że wybrany cytat nie został już wysłany temu samemu użytkownikowi w ciągu ostatnich 7 dni.
- pobierz_wczorajszy_cytat(sesja, user_id): Odpytuje historię, aby zwrócić cytat, który użytkownik otrzymał poprzedniego dnia.

W folderze znajdują się także pliki "seederów" wypełnijących tabele przykładowymi danymi do testów:
"users_seeder.py" dodaje 12 przykładowych kont użytkowników. Konta pokrywają wszystkie dostępne znaki zodiaku.
"quotes_seeder.py" dodaje 8 startowych cytatów, przypisując każdemu odpowiedniego autora oraz tag (np. pocieszajacy, motywacyjny).
"quotes_history_seeder.py" automatycznie generuje losową historię przypisywania cytatów do istniejących użytkowników (z ostatnich 30 dni). Skrypt jest kluczowy do prawidłowego przetestowania funkcji blokującej powtarzanie cytatów przez 7 dni.

NAJNOWSZA AKTUALIZACJA!!
W pliku database.py zostala dodana linijka odpowiadająca za inicjalizacje bazy danych poziom wyzej niz lokalizacja plikow inicjalizacyjnych. W zwiazku z tym mozna zpullowac sobie caly folder bazy danych i inicjalizować baze poza nim, wedlug schematu:
----baza_danych
|
|
----main.py (przykladowy plik importujący funkcje z database.py i seederow)
|
|
----database.db (tu stworzy sie plik database)

przykładowe zastosowanie funkcji z baza_danych w pliku main.py:
import sys
from pathlib import Path

#Kluczowa linijka! Sprawia, że Python widzi pliki z folderu baza_danych, można je swobodnie importować i testować bez wyskakiwania błędów ze ścieżkami.
sys.path.append(str(Path(__file__).resolve().parent / "baza_danych"))

#Importowanie konkretnych funkcji z danych plikow
from database import stworz_tabele
from users_seeder import seed_users
from quotes_seeder import seed_quotes
from quotes_history_seeder import seed_quote_history

def main():
    print("Inicjalizacja bazy danych i seederów...")
    stworz_tabele()
    seed_users()
    seed_quotes()
    seed_quote_history()
    print("Gotowe!")

if __name__ == "__main__":
    main()