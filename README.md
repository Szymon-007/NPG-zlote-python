Projekt npg zlote mysli na kazdy dzień

FRONTEND GUIDE:
/src:
	/pages:
		/Dashboard.jsx - określa dla domeny podstronę /dashboard, która jest ekranem wyświetlania cytatu
		/Login.jsx - określa dla domeny podstronę /login, która jest stroną logowania, pozwala na przejście hiperlinkiem do /register
		/Register.jsx - określa dla domeny podstronę /register, która jest stroną rejestracji użytkownika, pozwala na przejście hiperlinkiem do /login
		/Survey.jsx - określa dla domeny podstronę /survey, która jest stroną zawierającą ankietę co do humoru (buźki) itd
	/App.jsx:
		-główny plik określający cechy całej domeny
		-importuje funkcje wymagane do nawigowania po podstronach oraz dodaje te podstrony do domeny (przez import)
		-<BrowserRouter> <Routes> definiuje nawigację po podstronach, np:
		"<Route path="/" element={<Navigate to="/login" replace />} />
		<Route path="/login" element={<Login />} />" -- podstrona domyślna (sama domena bez podstrony) przenosi do /login które wykazuje 			funkcjonalność Login z pliku Login.jsx

JAK URUCHOMIĆ DOMENĘ LOCALHOST:
Musicie zainstalować Node.js (tam jest npm)

Wejdźcie na stronę nodejs.org
Pobierzcie i zainstalujcie wersję rekomendowaną (LTS).
Żeby sprawdzić czy działa, zrestartujcie terminal i wpiszcie 'node -v' oraz 'npm -v'.
Jeśli któraś z komend nie działa to musicie jeszcze wpisać 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser' i potwierdzić

oczywiście zróbcie git fetch i git checkout Nikodem, potrzebujecie całego mojego brancha
wszystko trzeba robić w folderze frontend, więc wpiszcie 'cd frontend'

następnie zainstalujcie potrzebne biblioteki, wystarczy w tym samym terminalu w frontend wpisać 'npm install' (wszystko zaintaluje automatycznie)

ostatnim krokiem jest wpisanie w terminalu 'npm run dev', to już stworzy localhosta, pokaże wam link i trzeba tylko go skopiować do paska adresu przeglądarki

JAK POWIĄZAĆ SWÓJ LOCALHOST I TOKEN Z FRONTENDEM:
spytajcie geminiego + wyślijcie mu:
src/utils/api.js ---> zawartość tekstową
"Frontend przekazał: Mój kod (w plikach Login.jsx i Register.jsx) wykonuje teraz strzały pod Wasz lokalny adres (ustawiłem domyślnie http://localhost:8000). Musicie wystawić tam dwa endpointy:

Logowanie: POST /api/login

Wysyłam JSON: {"email": "...", "password": "..."}

Oczekuję w odpowiedzi JSONa z kluczem: {"access_token": "tutaj_wasz_wygenerowany_jwt"}

Rejestracja: POST /api/register

Wysyłam JSON: {"email": "...", "password": "...", "name": "...", "zodiac_sign": "..."}
Oczekuję: Albo samego statusu 200/201 (wtedy user leci do ekranu logowania), albo od razu klucza access_token (wtedy loguję go automatycznie i wpuszczam do aplikacji).

Napisałem w pliku utils/api.js sprytny mechanizm dla funkcji Fetch. Gdy tylko wyślecie mi access_token, frontend sam zapisuje go w localStorage.

Od tego momentu każde kolejne zapytanie (np. o wysłanie ankiety) będzie miało automatycznie doklejony nagłówek:
Authorization: Bearer <token>

Odblokujcie CORS!
Ponieważ mój React działa na porcie 5173, a Wasze FastAPI na 8000, przeglądarka zablokuje naszą komunikację, dopóki tego nie włączycie.
Emil – upewnij się, że w głównym pliku FastAPI dodałeś CORSMiddleware i zezwoliłeś na ruch z http://localhost:5173 (metody, headery i credentials na True).

Jak postawicie te dwa endpointy i odpalicie u siebie serwer, to cały proces autoryzacji powinien nam już śmigać od deski do deski!"

PRZYKŁADOWY FORMAT JSON'A Z ODPOWIEDZIAMI W ANKIECIE: {"humor": "wesola", "stress": "niski", "motivation": "wysoka"}

OBSŁUGA BLOKADY STRON:
Jeśli nie ma ankiety z dzisiaj:
JSON {"has_filled_today": false}
Jeśli użytkownik wysłał już dzisiaj ankietę:
JSON {"has_filled_today": true}


