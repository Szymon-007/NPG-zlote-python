import { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { apiFetch, getToken } from '../utils/api';

export default function ProtectedRoute({ children }) {
  const token = getToken();
  const location = useLocation();
  const [loading, setLoading] = useState(true);
  const [hasFilledSurvey, setHasFilledSurvey] = useState(false);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    const checkSurveyStatus = async () => {
      try {
        const response = await apiFetch('/api/survey/status');
        if (response.ok) {
          const data = await response.json();
          setHasFilledSurvey(data.has_filled_today);
        }
      } catch (error) {
        console.error('Błąd sprawdzania statusu ankiety:', error);
      } finally {
        setLoading(false);
      }
    };

    checkSurveyStatus();
  }, [token, location.pathname]); 

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#DAEBE3] text-[#657166] font-bold text-lg">
        Sprawdzanie statusu sesji...
      </div>
    );
  }

  if (!hasFilledSurvey && location.pathname === '/dashboard') {
    return <Navigate to="/survey" replace />;
  }

  if (hasFilledSurvey && location.pathname === '/survey') {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}
