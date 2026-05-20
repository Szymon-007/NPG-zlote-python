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