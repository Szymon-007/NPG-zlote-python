import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch, removeToken } from '../utils/api';

export default function Dashboard() {
  const [quoteData, setQuoteData] = useState(null);
  const [loading, setLoading] = useState(true); // <--- Zaczynało się od ładowania 
 const navigate = useNavigate();

  useEffect(() => {
    const fetchDailyQuote = async () => {
      try {
        // Pytamy backend o wygenerowany na podstawie ankiety cytat
        const response = await apiFetch('/api/quote/daily');
        if (response.ok) {
          const data = await response.json();
          setQuoteData(data);
        } else {
          // Jeśli coś jest nie tak (np. brak ankiety), Guard i tak nas wyłapie, 
          // ale tutaj na wszelki wypadek dajemy fallback
          console.error("Nie udało się pobrać cytatu");
        }
      } catch (error) {
        console.error("Błąd połączenia:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDailyQuote();
  }, []);

  const handleLogout = () => {
    removeToken(); // Czyścimy JWT z localStorage
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#DAEBE3] text-[#657166] font-bold">
        Przygotowujemy Twój cytat...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#DAEBE3] flex flex-col items-center p-6">
      
      {/* Pasek Nawigacyjny / Header */}
      <div className="w-full max-w-4xl flex justify-between items-center mb-12 mt-4">
        <h2 className="text-2xl font-bold !text-[#657166] tracking-tight">Twój Cytat</h2>
        <button 
          onClick={handleLogout}
          className="px-6 py-2 bg-white text-[#657166] font-bold rounded-xl shadow-sm hover:bg-[#F3C3B2] transition-colors"
        >
          Wyloguj
        </button>
      </div>

      {/* GŁÓWNA KARTA Z CYTATEM */}
      <div className="bg-white w-full max-w-2xl p-12 rounded-[3rem] shadow-2xl text-center relative overflow-hidden">
        
        {/* Dekoracyjny element w tle karty */}
        <div className="absolute top-[-20px] left-[-20px] w-32 h-32 bg-[#FDE8D3] rounded-full opacity-50"></div>
        
        <div className="relative z-10">
          <span className="text-6xl text-[#99CDD8] font-serif opacity-50 block mb-4">“</span>
          
          <h1 className="text-3xl md:text-4xl font-medium !text-[#657166] leading-relaxed italic mb-8">
            {quoteData?.text || "Dobrego dnia! Pamiętaj, że każdy krok przybliża Cię do celu."}
          </h1>
          
          <div className="w-16 h-1 bg-[#F3C3B2] mx-auto mb-6"></div>
          
          <p className="text-[#657166] font-bold text-xl uppercase tracking-widest">
            {quoteData?.author || "Twój Asystent"}
          </p>
          
          {/* Informacja o dopasowaniu (opcjonalnie) */}
          <div className="mt-8 inline-block px-4 py-1 bg-[#DAEBE3] rounded-full text-xs font-bold text-[#657166]/70">
            Dopasowano do Twojego nastroju: {quoteData?.category || "Energia"}
          </div>
        </div>

        <span className="!absolute bottom-[+5px] right-4 text-6xl text-[#99CDD8] font-serif opacity-50 block rotate-180">“</span>
      </div>

      {/* Dodatkowy przycisk na dole */}
      <p className="mt-12 text-[#657166]/60 text-sm font-medium">
        Wróć jutro po nową dawkę motywacji!
      </p>
      
    </div>
  );
}