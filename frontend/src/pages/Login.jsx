import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { apiFetch, setToken } from '../utils/api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMessage(''); 

    try {
      const response = await apiFetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        setToken(data.access_token);
        
        navigate('/survey'); 
      } else {
        setErrorMessage('Nieprawidłowy e-mail lub hasło.');
      }
    } catch (error) {
      setErrorMessage('Błąd połączenia z serwerem. Spróbuj ponownie.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#DAEBE3] p-4">
      <div className="bg-white p-10 rounded-2xl shadow-xl w-full max-w-md text-[#657166]">
        <h1 className="text-3xl font-bold text-center mb-8 !text-[#FDE8D3]">Zaloguj się</h1>

     
        <form onSubmit={handleLogin} className="flex flex-col gap-5">
          
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

         
          {errorMessage && (
            <div className="text-red-500 text-sm font-bold text-center">
              {errorMessage}
            </div>
          )}

          <button
            type="submit"
            className="w-full p-4 mt-4 bg-[#99CDD8] hover:bg-[#657166] hover:text-white text-[#657166] font-bold rounded-xl transition-colors text-lg shadow-sm"
          >
            Wejdź
          </button>
        </form>

        <div className="mt-8 text-center">
          <Link to="/register" className="text-sm font-medium hover:text-[#F3C3B2] transition-colors">
            Nie masz jeszcze konta? <span className="underline">Zarejestruj się</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
