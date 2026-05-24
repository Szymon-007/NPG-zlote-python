import { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { apiFetch, getToken } from '../utils/api';

export default function ProtectedRoute({ children }) {
  const token = getToken();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [hasFilledSurvey, setHasFilledSurvey] = useState(false);

  useEffect(() => {
    // Jeśli nie ma tokenu, nie ma nawet po co pytać backendu
    if (!token) {
      setLoading(false);
      return;
    }

    const checkSurveyStatus = async () => {
      try {
        // Pytamy backend, czy zalogowany user wysłał już dzisiaj ankietę
        const response = await apiFetch('/api/survey/status');
        if (response.ok) {
          const data = await response.json();
          // Oczekujemy od chłopaków booleana: true lub false
          setHasFilledSurvey(data.has_filled_today);
        }
      } catch (error) {
        console.error('Błąd sprawdzania statusu ankiety:', error);
      } finally {
        setLoading(false);
      }
    };

    checkSurveyStatus();
  }, [token, location.pathname]); // Sprawdzaj status przy każdej zmianie podstrony

  // 1. OCHRONA LOGOWANIA: Brak tokenu? Wjazd wzbroniony, kierunek logowanie
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // 2. EKRAN ŁADOWANIA: Zanim backend odpowie, pokazujemy krótkie info
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#DAEBE3] text-[#657166] font-bold text-lg">
        Sprawdzanie statusu sesji...
      </div>
    );
  }

  // 3. LOGIKA GUARDA (Właściwa blokada ankiety)
  
  // Przypadek A: Użytkownik NIE wypełnił ankiety, a próbuje wejść na /dashboard
  if (!hasFilledSurvey && location.pathname === '/dashboard') {
    return <Navigate to="/survey" replace />;
  }

  // Przypadek B: Użytkownik JUŻ wypełnił ankietę, a próbuje wejść ponownie na /survey
  if (hasFilledSurvey && location.pathname === '/survey') {
    return <Navigate to="/dashboard" replace />;
  }

  // Jeśli wszystko jest w porządku, pozwól wyrenderować stronę (children)
  return children;
}