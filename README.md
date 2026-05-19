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

