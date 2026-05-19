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




