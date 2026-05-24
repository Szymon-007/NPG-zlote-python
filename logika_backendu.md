# ⚙️ Dokumentacja logiki backendu: Ankieta i Losowanie Cytatow

Ponizszy dokument opisuje przeplyw danych, algorytm wyliczania tagow oraz mechanizm losowania cytatow w oparciu o codzienne ankiety uzytkownikow.

---

## 1. Glowny endpoint: `/losuj-cytat` (POST)

Jest to serce modulu ankiet. Endpoint przyjmuje odpowiedzi uzytkownika z frontendu i na ich podstawie zwraca idealnie dopasowany cytat.

**Wymagania:**
* Endpoint jest zabezpieczony - wymaga przekazania tokena JWT zalogowanego uzytkownika (Bearer Token).
* Przyjmuje w body obiekt ankiety (`PollSubmit`), ktory zawiera trzy parametry w formacie `MoodEnum` (bardzo, srednio, bardzo_nie):
    * `stress` (poziom stresu)
    * `motivation` (poziom motywacji)
    * `mood` (ogolne samopoczucie)

**Dzialanie:**
1. Apka na backendzie **nie zapisuje** odpowiedzi uzytkownika do bazy danych. Sluza one jedynie do jednorazowego wyliczenia tagu.
2. Odpala sie algorytm wyliczajacy odpowiedni tag cytatu.
3. System odpytuje baze danych o cytat pasujacy do tagu, pilnujac, by uniknac powtorek.
4. Zapisuje w historii (`QuoteHistory`) wylacznie informacje o tym, jaki cytat zostal wylosowany dla danego uzytkownika w danym dniu.

---

## 2. Algorytm wyliczania tagu (Drzewo decyzyjne)

Algorytm opiera sie na priorytetyzacji emocji. Dziala na zasadzie instrukcji warunkowych (if/elif/else), sprawdzajac parametry w ustalonej kolejnosci:

1. **Priorytet 1 (Stres):** Jesli `stress == bardzo_nie`, system natychmiast przerywa sprawdzanie i zwraca tag **"odstresowujacy"**. Ignoruje przy tym poziom motywacji i samopoczucia.
2. **Priorytet 2 (Motywacja):** Jesli stres jest w normie, a `motivation == bardzo_nie`, algorytm przypisuje tag **"motywacyjny"**.
3. **Priorytet 3 (Samopoczucie):** Jesli stres i motywacja sa okej, ale `mood == bardzo_nie`, zwracany jest tag **"pocieszajacy"**.
4. **Wariant optymistyczny (Fallback):** Jesli zaden z powyzszych warunkow krytycznych nie zostal spelniony (uzytkownik czuje sie dobrze), algorytm zwraca domyslny tag **"ogolny cytat refleksyjny"**.

---

## 3. Logika losowania i zapobiegania powtorkom

Aby uzytkownik nie dostawal w kolko tych samych cytatow, proces losowania jest zabezpieczony odpowiednimi mechanizmami bazodanowymi:

* **Blokada 7-dniowa:** Baza danych filtruje cytaty pasujace do wyliczonego tagu. Nastepnie sprawdza tabele historii (`QuoteHistory`) i za pomoca instrukcji `NOT IN` odrzuca te cytaty, ktore uzytkownik otrzymal w ciagu ostatnich 7 dni.
* **Losowanie awaryjne (Bezpiecznik):** Jesli w wyniku dzialania filtra 7-dniowego pula dostepnych cytatow jest pusta (uzytkownik wyczerpal "swieze" cytaty dla danego tagu), system awaryjnie ignoruje historie i losuje cytat z calej dostepnej puli dla tego tagu.
* Jesli w bazie w ogole brakuje cytatow z danym tagiem, system ratuje sie losowaniem calkowicie w ciemno z calej tabeli `Quote`.

Dzieki temu frontend nigdy nie otrzymuje pustej odpowiedzi i zawsze ma co wyswietlic uzytkownikowi.

---

## 4. Obsluga wyjatkow i bezpieczenstwo

Cala logika operacji na bazie danych (SQLite) zabezpieczona jest globalnym "lapaczem bledow" (Exception Handler).

W przypadku awarii bazy (np. brak polaczenia, blad zapisu), FastAPI wylapuje `SQLAlchemyError` i zamiast "wysypac" aplikacje oraz pokazac wrazliwe dane serwera (stack trace), zwraca bezpieczny komunikat HTTP 500 z prosba o ponowna probe pozniej.