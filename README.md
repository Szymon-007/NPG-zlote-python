# Złote myśli na każdy dzień

Projekt zrobiony na zajęcia z NPG. To prosta aplikacja webowa, która codziennie losuje użytkownikowi cytat dopasowany do jego samopoczucia. Po zalogowaniu wypełnia się krótką ankietę (humor, stres, motywacja), a na tej podstawie backend wybiera kategorię cytatu i losuje z niej coś, czego użytkownik nie dostał w ciągu ostatniego tygodnia. Do tego jest osobny skrypt, który rozsyła cytaty mailem.

Całość składa się z trzech części:

- backend w Pythonie (FastAPI + SQLModel, baza SQLite),
- frontend w React (Vite + Tailwind),
- skrypt do wysyłki maili przez Gmaila.

## Jak to działa

1. Użytkownik zakłada konto na `/register` (email, hasło, imię, znak zodiaku). Hasło jest hashowane bcryptem, a backend od razu zwraca token JWT, więc po rejestracji nie trzeba się osobno logować.
2. Token trafia do `localStorage` w przeglądarce i jest doklejany do każdego kolejnego zapytania jako nagłówek `Authorization: Bearer ...`. Token jest ważny 30 minut.
3. Po zalogowaniu frontend pyta backend, czy użytkownik wypełnił już dzisiaj ankietę. Jeśli nie, przekierowuje na `/survey`, a jeśli tak, to od razu na `/dashboard`. Ankietę da się więc wypełnić tylko raz dziennie.
4. Z odpowiedzi w ankiecie liczony jest tag cytatu (`app/script.py`). Reguły są proste i sprawdzane po kolei:
   - wysoki stres → `odstresowujacy`
   - niska motywacja → `motywacyjny`
   - smutny humor → `pocieszajacy`
   - w pozostałych przypadkach → `ogolny`
5. Backend losuje cytat z tym tagiem, pomijając te, które użytkownik dostał w ciągu ostatnich 7 dni. Jak nie ma już nic nowego, bierze dowolny cytat z tej kategorii, a w ostateczności dowolny cytat z bazy. Wylosowany cytat zapisuje się w tabeli `QuoteHistory`.
6. Dashboard pobiera ostatni wpis z historii i wyświetla cytat razem z autorem i kategorią.

## Struktura projektu

```
NPG-zlote-python/
├── app/                  backend (FastAPI)
├── baza_danych/          modele, połączenie z bazą, funkcje CRUD, seedery
├── frontend/             aplikacja w React
├── email_send.py         wysyłka cytatów mailem
├── email_template.html   szablon maila
├── requirements.txt      zależności Pythona
├── HOWTO.md              stare, skrócone notatki jak odpalić
└── .env                  dane do konta Gmail (NADAWCA, HASLO_APLIKACJI)
```

### app/

- **main.py** - główny plik serwera. Tworzy aplikację FastAPI, włącza CORS dla `localhost:5173` (tam chodzi frontend) i przy starcie tworzy tabele w bazie. Są tu wszystkie endpointy:
  - `POST /api/register` - rejestracja, zwraca token,
  - `POST /api/login` - logowanie, zwraca token,
  - `GET /api/survey/status` - czy użytkownik wypełnił dziś ankietę (`{"has_filled_today": true/false}`),
  - `POST /api/survey` - przyjmuje odpowiedzi z ankiety, zapisuje datę, losuje cytat i dopisuje go do historii,
  - `GET /api/quote/daily` - zwraca ostatnio wylosowany cytat (`text`, `author`, `category`).

  Tutaj są też funkcje do hashowania i sprawdzania haseł (passlib + bcrypt).
- **JWTgen.py** - tworzenie i weryfikacja tokenów JWT. `create_access_token` generuje token z mailem i id użytkownika, a `get_current_user` jest używany jako zależność w chronionych endpointach: dekoduje token i wyciąga użytkownika z bazy, a jak coś się nie zgadza, zwraca 401.
- **models_mimics.py** - modele Pydantic do walidacji tego, co przychodzi z frontendu (`UserRegister`, `UserLogin`, `PollSubmit`). Jest tu też model `Poll`, który miał przechowywać ankiety, ale ostatecznie nie jest nigdzie używany.
- **script.py** - funkcja `calculate_ideal_tag`, czyli logika wybierania kategorii cytatu na podstawie ankiety (opisana wyżej).

### baza_danych/

- **models.py** - definicje tabel:
  - `User` - id, email, hash hasła, znak zodiaku, data ostatniej ankiety,
  - `Quote` - treść, autor, tag,
  - `QuoteHistory` - który użytkownik dostał który cytat i kiedy (klucze obce do `User` i `Quote`).

  Oprócz tego są tu enumy `ZodiacSign` (12 znaków) i `QuoteTag` (4 kategorie).
- **database.py** - połączenie z SQLite. Plik bazy `database.db` tworzy się w głównym folderze projektu. `pobierz_sesje` jest używane w FastAPI do wstrzykiwania sesji do endpointów. Odpalony bezpośrednio tworzy same tabele.
- **crud.py** - funkcje do operacji na bazie: dodawanie i wyszukiwanie użytkowników, aktualizacja daty ankiety, losowanie cytatu bez powtórek z ostatnich 7 dni, zapis do historii i pobieranie "wczorajszego" cytatu dla maili.
- **quotes_seeder.py** - wrzuca do bazy 152 cytaty, po 38 na każdą kategorię. Jeśli w bazie są już jakieś cytaty, nic nie robi.
- **users_seeder.py** - miał dodawać 12 testowych kont, ale w obecnej wersji nie działa (szczegóły niżej, w sekcji o znanych problemach).
- **quotes_history_seeder.py** - generuje losową historię cytatów dla istniejących użytkowników (po 3 wpisy z ostatnich 30 dni). Przydaje się do testowania blokady powtórek.
- **db_health_check.py** - wypisuje, ile jest użytkowników, cytatów i wpisów w historii, i sprawdza, czy w historii nie ma odwołań do nieistniejących rekordów.
- **README.md** - dokładniejszy opis samej bazy i relacji między tabelami.

### frontend/

- **src/main.jsx** - punkt wejścia Reacta.
- **src/App.jsx** - routing. `/` przekierowuje na `/login`, a `/survey` i `/dashboard` są opakowane w `ProtectedRoute`.
- **src/components/ProtectedRoute.jsx** - pilnuje dostępu do chronionych stron. Bez tokena wyrzuca na logowanie, a z tokenem sprawdza status ankiety i przekierowuje między `/survey` a `/dashboard` tak, żeby nie dało się wypełnić ankiety dwa razy ani wejść na dashboard przed jej wypełnieniem.
- **src/utils/api.js** - funkcja `apiFetch`, czyli wrapper na `fetch`, który dokleja token i adres backendu (`http://localhost:8000`). Przy odpowiedzi 401 usuwa token i przenosi na stronę logowania. Są tu też funkcje do zapisu, odczytu i usuwania tokena.
- **src/pages/Login.jsx** - formularz logowania.
- **src/pages/Register.jsx** - formularz rejestracji z wyborem znaku zodiaku.
- **src/pages/Survey.jsx** - ankieta z trzema pytaniami, w każdym trzy przyciski z buźkami do wyboru.
- **src/pages/Dashboard.jsx** - wyświetla wylosowany cytat i przycisk wylogowania.
- **README.md** - notatki frontendowca dla reszty zespołu (format JSON-ów, jak odpalić frontend).

### Wysyłka maili

- **email_send.py** - przy pierwszym uruchomieniu tworzy bazę i wrzuca do niej cytaty, jeśli jeszcze jej nie ma. Potem łączy się z Gmailem przez SMTP i do każdego użytkownika z bazy (maksymalnie 40 naraz) wysyła maila z cytatem z jego historii i linkiem do strony logowania. W kodzie jest też zakomentowana wersja z APSchedulerem, która wysyłałaby maile codziennie o 8:00.
- **email_template.html** - szablon maila w HTML. Pola `$cytat`, `$autor` i `$link` są podmieniane przez `string.Template`.

## Jak odpalić

Potrzebny jest Python 3.10 lub nowszy (w kodzie są typy w stylu `int | None`) i Node.js (wersja LTS, razem z nim instaluje się npm). Komendy poniżej są pod PowerShella na Windowsie i wszystkie odpala się z głównego folderu projektu, chyba że napisane jest inaczej.

### 1. Backend

Tworzymy wirtualne środowisko i instalujemy zależności:

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

Wrzucamy cytaty do bazy. Seedery trzeba odpalać jako moduły (`-m`) z głównego folderu, inaczej nie zadziałają importy z `baza_danych`:

```bash
python -m baza_danych.quotes_seeder
```

Odpalamy serwer:

```bash
python -m uvicorn app.main:app --reload
```

Backend będzie działał pod `http://localhost:8000`, a automatyczna dokumentacja API od FastAPI jest pod `http://localhost:8000/docs`.

### 2. Frontend

W drugim terminalu:

```bash
cd frontend
```

```bash
npm install
```

```bash
npm run dev
```

Strona będzie dostępna pod `http://localhost:5173`. Trzeba wejść dokładnie pod ten adres, bo backend ma CORS ustawiony tylko na ten port.

Jeśli PowerShell nie pozwala odpalić `npm`, pomaga jednorazowo:

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Wysyłka maili (opcjonalnie)

Do wysyłki potrzebne jest konto Gmail z włączoną weryfikacją dwuetapową i wygenerowanym hasłem aplikacji (Konto Google → Bezpieczeństwo → Hasła do aplikacji). W pliku `.env` w głównym folderze wpisujemy:

```
NADAWCA=twoj.adres@gmail.com
HASLO_APLIKACJI=haslo_aplikacji_z_google
```

I odpalamy:

```bash
python email_send.py
```

Maile pójdą do wszystkich użytkowników, którzy są w bazie, więc przy testach lepiej mieć tam tylko własne konta.

### Sprawdzenie bazy

```bash
python -m baza_danych.db_health_check
```
