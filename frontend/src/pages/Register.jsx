import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { apiFetch, setToken } from '../utils/api';

export default function Register() {
  // 1. Zmienne stanu dla wszystkich pól (zauważ, że zodiacSign startuje jako pusty string)
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [zodiacSign, setZodiacSign] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();

  // 2. Funkcja obsługująca wysyłkę formularza
  const handleRegister = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    // Ręczna walidacja, żeby nie wysłać formularza bez znaku zodiaku
    if (!zodiacSign) {
      setErrorMessage('Proszę wybrać znak zodiaku.');
      return;
    }

    try {
      // 3. Strzał do endpointu rejestracji
      const response = await apiFetch('/api/register', {
        method: 'POST',
        body: JSON.stringify({
          email: email,
          password: password,
          name: name,
          zodiac_sign: zodiacSign // Używamy snake_case, żeby ułatwić życie chłopakom od Pythona
        })
      });

      if (response.ok) {
        // Czasem backend po rejestracji od razu loguje użytkownika i daje token
        const data = await response.json().catch(() => ({})); 
        
        if (data.access_token) {
          setToken(data.access_token);
          navigate('/survey'); // Jeśli jest token -> od razu do ankiety
        } else {
          navigate('/login'); // Jeśli nie ma tokenu -> wyślij na ekran logowania
        }
      } else {
        // Próba odczytania wiadomości o błędzie z backendu (np. "Konto już istnieje")
        const errorData = await response.json().catch(() => null);
        setErrorMessage(errorData?.detail || 'Błąd podczas rejestracji. Spróbuj ponownie.');
      }
    } catch (error) {
      setErrorMessage('Błąd połączenia z serwerem. Spróbuj ponownie.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#DAEBE3] p-4">
      <div className="bg-white p-10 rounded-2xl shadow-xl w-full max-w-md text-[#657166]">
        <h1 className="text-3xl font-bold text-center mb-8 !text-[#FDE8D3]">Rejestracja</h1>

        {/* Podpinamy funkcję pod formularz */}
        <form onSubmit={handleRegister} className="flex flex-col gap-4">
          
          <input
            type="email"
            placeholder="Adres e-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full p-4 bg-[#FDE8D3] rounded-xl outline-none focus:ring-4 focus:ring-[#99CDD8]/50 text-[#657166] placeholder-[#657166]/60 transition-all font-medium"
          />
          
          <input
            type="password"
            placeholder="Hasło"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full p-4 bg-[#FDE8D3] rounded-xl outline-none focus:ring-4 focus:ring-[#99CDD8]/50 text-[#657166] placeholder-[#657166]/60 transition-all font-medium"
          />
          
          <input
            type="text"
            placeholder="Twoje imię"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="w-full p-4 bg-[#FDE8D3] rounded-xl outline-none focus:ring-4 focus:ring-[#99CDD8]/50 text-[#657166] placeholder-[#657166]/60 transition-all font-medium"
          />

          <select
            value={zodiacSign}
            onChange={(e) => setZodiacSign(e.target.value)}
            className="w-full p-4 bg-[#FDE8D3] rounded-xl outline-none focus:ring-4 focus:ring-[#99CDD8]/50 text-[#657166] transition-all font-medium cursor-pointer"
          >
            <option value="" disabled>Wybierz znak zodiaku</option>
            <option value="baran">Baran</option>
            <option value="byk">Byk</option>
            <option value="bliznieta">Bliźnięta</option>
            <option value="rak">Rak</option>
            <option value="lew">Lew</option>
            <option value="panna">Panna</option>
            <option value="waga">Waga</option>
            <option value="skorpion">Skorpion</option>
            <option value="strzelec">Strzelec</option>
            <option value="koziorozec">Koziorożec</option>
            <option value="wodnik">Wodnik</option>
            <option value="ryby">Ryby</option>
          </select>

          {/* Wyświetlanie błędów pod formularzem */}
          {errorMessage && (
            <div className="text-red-500 text-sm font-bold text-center">
              {errorMessage}
            </div>
          )}

          <button
            type="submit"
            className="w-full p-4 mt-4 bg-[#F3C3B2] hover:bg-[#657166] hover:text-white text-[#657166] font-bold rounded-xl transition-colors text-lg shadow-sm"
          >
            Załóż konto
          </button>
        </form>

        <div className="mt-8 text-center">
          <Link to="/login" className="text-sm font-medium hover:text-[#99CDD8] transition-colors">
            Masz już konto? <span className="underline">Zaloguj się</span>
          </Link>
        </div>
      </div>
    </div>
  );
}