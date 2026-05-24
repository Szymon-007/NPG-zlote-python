# Moduł Bazy Danych

Folder składa się z trzech plików inicjalizujących bazę danych, a w niej trzy tabele:
1. **Tabela użytkowników** (`User`)
2. **Tabela cytatów** (`Quote`)
3. **Historia cytatów** (`QuoteHistory`)

## Architektura i Relacje (Klucze Obce)

Baza danych opiera się na relacyjnym modelu, w którym głównym punktem łączącym (tzw. tabelą asocjacyjną) jest `QuoteHistory`. Tabele są połączone za pomocą następujących kluczy obcych (Foreign Keys):

* **`QuoteHistory.user_id` -> `User.id`**
  Tworzy relację jeden-do-wielu (1:N). Jeden użytkownik może mieć wiele wpisów w historii (otrzymać wiele cytatów), ale konkretny wpis w historii należy tylko do jednego użytkownika. Zapewnia to identyfikację, do kogo trafił dany cytat.
  
* **`QuoteHistory.quote_id` -> `Quote.id`**
  Tworzy relację jeden-do-wielu (1:N). Jeden cytat może zostać wylosowany i przypisany do wielu różnych użytkowników w różnym czasie, ale dany wpis w historii zawsze odnosi się do jednego, konkretnego cytatu z bazy.

Za inicjalizację odpowiadają dwa pliki:
* `database.py` – wywołanie tego pliku powoduje stworzenie bazy danych lokalnie.
* `models.py` – plik podrzędny opisujący struktury tabel; w linijkach 26-45 opisane są nazwy i kolumny poszczególnych tabel.

---

## Funkcje CRUD (`crud.py`)

Plik `crud.py` zawiera zestaw funkcji potrzebnych do wykonywania operacji na bazie danych; są to kolejno:

* **`zapisz_cytat_do_historii(sesja, user_id, quote_id)`**
  Zapisuje w bazie fakt, że dany użytkownik otrzymał konkretny cytat (dodaje wpis z obecną datą).

* **`pobierz_uzytkownika_po_mailu(sesja, email)`**
  Wyszukuje i zwraca obiekt użytkownika na podstawie jego adresu email.

* **`dodaj_uzytkownika(sesja, email, hash_haslo, zodiak)`**
  Tworzy nowego użytkownika w tabeli "User" i od razu go zwraca.

* **`pobierz_cytat_po_tagu_bez_powtorek7(sesja, user_id, tag)`**
  Główna funkcja do losowania cytatu. Filtruje cytaty po wybranym tagu i upewnia się, że wybrany cytat nie został już wysłany temu samemu użytkownikowi w ciągu ostatnich 7 dni.

* **`pobierz_wczorajszy_cytat(sesja, user_id)`**
  Odpytuje historię, aby zwrócić cytat, który użytkownik otrzymał poprzedniego dnia.

---

## Seedery

W folderze znajdują się także pliki "seederów" wypełniających tabele przykładowymi danymi do testów:

* **`users_seeder.py`** – Dodaje 12 przykładowych kont użytkowników. Konta pokrywają wszystkie dostępne znaki zodiaku.
* **`quotes_seeder.py`** – Dodaje 8 startowych cytatów, przypisując każdemu odpowiedniego autora oraz tag (np. pocieszajacy, motywacyjny).
* **`quotes_history_seeder.py`** – Automatycznie generuje losową historię przypisywania cytatów do istniejących użytkowników (z ostatnich 30 dni). Skrypt jest kluczowy do prawidłowego przetestowania funkcji blokującej powtarzanie cytatów przez 7 dni.

---

## NAJNOWSZA AKTUALIZACJA!!

W pliku `database.py` została dodana linijka odpowiadająca za inicjalizacje bazy danych poziom wyżej niż lokalizacja plików inicjalizacyjnych. W związku z tym można zpullować sobie cały folder bazy danych i inicjalizować bazę poza nim, według schematu:

```text
----baza_danych/
|
----main.py (przykładowy plik importujący funkcje z database.py i seederow)
|
----database.db (tu stworzy sie plik database)