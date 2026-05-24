import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch } from '../utils/api';

export default function Survey() {
  const navigate = useNavigate();

  // 1. Jeden wspólny stan (useState) przechowujący wszystkie 3 wybory
  const [answers, setAnswers] = useState({
    humor: '',
    stress: '',
    motivation: ''
  });
  
  const [errorMessage, setErrorMessage] = useState('');

  // 2. Funkcja aktualizująca wybrany stan po kliknięciu minki
  const handleSelect = (category, value) => {
    setAnswers((prev) => ({ ...prev, [category]: value }));
    setErrorMessage(''); // Czyścimy błąd, gdy użytkownik coś kliknie
  };

  // 3. Obsługa wysłania ankiety
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Sprawdzamy, czy użytkownik zaznaczył wszystko
    if (!answers.humor || !answers.stress || !answers.motivation) {
      setErrorMessage('Proszę, wybierz jedną opcję w każdej kategorii!');
      return;
    }

    try {
      // Używamy naszego inteligentnego kuriera, który sam doda token z localStorage
      const response = await apiFetch('/api/survey', {
        method: 'POST',
        body: JSON.stringify(answers)
      });

      if (response.ok) {
  const wylosowanyCytat = await response.json(); // Wyciągasz cytat, który backend właśnie przysłał
  navigate('/dashboard', { state: { cytat: wylosowanyCytat } }); // Idziesz na dashboard i niesiesz ten cytat ze sobą
}
    } catch (error) {
      setErrorMessage('Błąd serwera. Sprawdź połączenie.');
    }
  };

  // 4. Funkcja pomocnicza rysująca pojedynczy kafelkowy przycisk
  const renderEmojiButton = (category, value, emoji, label) => {
    // Sprawdzamy, czy ten konkretny przycisk jest obecnie wybrany
    const isSelected = answers[category] === value;

    return (
      <button
        type="button"
        onClick={() => handleSelect(category, value)}
        className={`flex flex-col items-center justify-center p-3 rounded-2xl transition-all duration-300 ${
          isSelected 
            ? 'bg-[#99CDD8] scale-110 shadow-lg ring-2 ring-[#657166]' // Wygląd ZAZNACZONEGO
            : 'bg-[#FDE8D3] hover:bg-[#CFD6C4] hover:scale-105 opacity-80' // Wygląd ODPOCZYWAJĄCEGO
        }`}
      >
        <span className="text-4xl mb-2">{emoji}</span>
        <span className="text-xs font-bold text-[#657166] uppercase tracking-wider">{label}</span>
      </button>
    );
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#DAEBE3] p-4">
      <div className="bg-white p-8 sm:p-10 rounded-3xl shadow-xl w-full max-w-lg text-[#657166]">

        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2 text-[#FDE8D3] !text-[#657166]">Jak się dzisiaj czujesz?</h1>
          <p className="text-sm text-gray-500">Dopasujemy idealny cytat do Twojego obecnego nastroju.</p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-8">

          {/* Kategoria 1: Poczucie Humoru */}
          <div className="flex flex-col gap-3">
            <h3 className="font-bold text-lg text-center">Poczucie humoru</h3>
            <div className="grid grid-cols-3 gap-4">
              {renderEmojiButton('humor', 'smutna', '😞', 'Słabo')}
              {renderEmojiButton('humor', 'neutralna', '😐', 'Neutralnie')}
              {renderEmojiButton('humor', 'wesola', '😄', 'Świetnie')}
            </div>
          </div>

          {/* Kategoria 2: Poziom Stresu */}
          <div className="flex flex-col gap-3">
            <h3 className="font-bold text-lg text-center">Poziom stresu</h3>
            <div className="grid grid-cols-3 gap-4">
              {renderEmojiButton('stress', 'niski', '😌', 'Niski')}
              {renderEmojiButton('stress', 'sredni', '😬', 'Średni')}
              {renderEmojiButton('stress', 'wysoki', '🤯', 'Wysoki')}
            </div>
          </div>

          {/* Kategoria 3: Poziom Motywacji */}
          <div className="flex flex-col gap-3">
            <h3 className="font-bold text-lg text-center">Poziom motywacji</h3>
            <div className="grid grid-cols-3 gap-4">
              {renderEmojiButton('motivation', 'niska', '🥱', 'Niska')}
              {renderEmojiButton('motivation', 'srednia', '🤔', 'Średnia')}
              {renderEmojiButton('motivation', 'wysoka', '🚀', 'Wysoka')}
            </div>
          </div>

          {/* Wyświetlanie błędu (np. gdy ktoś nie kliknie wszystkich 3) */}
          {errorMessage && (
            <div className="text-red-500 text-sm font-bold text-center mt-2">
              {errorMessage}
            </div>
          )}

          {/* Przycisk wysyłania (pojawia się wizualnie jako aktywny, gdy wszystko wyklikano) */}
          <button
            type="submit"
            className={`w-full p-4 mt-2 font-bold rounded-xl transition-colors text-lg shadow-sm ${
              answers.humor && answers.stress && answers.motivation
                ? 'bg-[#F3C3B2] hover:bg-[#657166] hover:text-white text-[#657166]'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
          >
            Losuj mój cytat!
          </button>
        </form>

      </div>
    </div>
  );
}