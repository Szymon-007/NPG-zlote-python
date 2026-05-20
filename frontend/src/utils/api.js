// 1. Funkcje do zarządzania tokenem w pamięci przeglądarki (localStorage)
export const setToken = (token) => localStorage.setItem('jwt_token', token);
export const getToken = () => localStorage.getItem('jwt_token');
export const removeToken = () => localStorage.removeItem('jwt_token');

// Główny adres serwera FastAPI chłopaków z backendu (domyślnie u nich to port 8000)
const API_BASE_URL = 'http://localhost:8000';

// 2. Nasz "Sprytny Fetch" - automatycznie dokleja JWT do każdego zapytania
export const apiFetch = async (endpoint, options = {}) => {
  // Pobieramy bilet z pamięci
  const token = getToken();

  // Konfigurujemy domyślne nagłówki (mówimy, że wysyłamy JSON)
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Jeśli mamy token, autouzupełniamy nagłówek autoryzacji
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Wykonujemy właściwy strzał do API
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Zabezpieczenie: Jeśli backend odpowie błędem 401 (Nieautoryzowany / Token wygasł)
  if (response.status === 401) {
    removeToken(); // Czyścimy stary token
    window.location.href = '/login'; // Wyrzucamy usera do logowania
  }

  return response;
};