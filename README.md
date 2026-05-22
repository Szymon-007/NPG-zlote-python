# Instrukcja Wdrożenia i Uruchomienia Projektu

Niniejszy dokument opisuje kroki niezbędne do poprawnego uruchomienia aplikacji bezpośrednio po sklonowaniu repozytorium z GitHub.

---

## CZĘŚĆ 1: BACKEND (FastAPI)

Wszystkie komendy w tej sekcji wykonuj **w głównym folderze projektu** (`C:\Users\escib\PyCharmProjects\zlote_mysli_npg`). Nie wchodź do folderu `app`.

### 1. Przygotowanie środowiska i instalacja bibliotek
Upewnij się, że instalujesz biblioteki wewnątrz środowiska wirtualnego, aby uniknąć błędu `ModuleNotFoundError: No module named 'sqlmodel'`.

```bash
# 1. Aktywacja środowiska wirtualnego
.venv\Scripts\activate

# 2. Instalacja wszystkich wymaganych pakietów backendowych
python -m pip install --upgrade pip
pip install sqlmodel fastapi uvicorn passlib[bcrypt] python-jose[cryptography] bcrypt==4.0.1
```
### 2. Zasilenie bazy danych (Seedery)
Wykonaj te komendy z głównego folderu, aby skrypty poprawnie widziały moduł baza_danych. Zapobiegnie to błędowi ModuleNotFoundError: No module named 'baza_danych'.
```bash
python users_seeder.py
python baza_danych/quotes_seeder.py
python baza_danych/quotes_history_seeder.py
```
### 3. Uruchomienie serwera API
Aby uvicorn prawidłowo odnalazł aplikację i ścieżki importów, musisz wskazać moduł jako app.main:app (wywołanie samego main:app spowoduje błąd importu aplikacji ASGI).
```bash
python -m uvicorn app.main:app --reload
Adres serwera: http://127.0.0.1:8000
Dokumentacja i testowanie endpointów: http://127.0.0.1:8000/docs
```
### Dodatkowo niezbędne są do dokonania następujące zmiany w plikach zespołu:
- w pliku baza_danych/models.py w funkcji ZodiacSign nazwy znaków zodiaku muszą rozpoczynać się z duzej litery aby być spójne z frontendem
- w pliku crud.py zmienic importpliku models na baza_danych.models
- taki sposób importu innych plików musi byc zachowany absulotnie w każdym pliku projektu, backend odpala się z głownego katalogu
