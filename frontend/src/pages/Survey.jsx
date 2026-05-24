import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch } from '../utils/api';

export default function Survey() {
  const navigate = useNavigate();

  const [answers, setAnswers] = useState({
    humor: '',
    stress: '',
    motivation: ''
  });
  
  const [errorMessage, setErrorMessage] = useState('');

  const handleSelect = (category, value) => {
    setAnswers((prev) => ({ ...prev, [category]: value }));
    setErrorMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!answers.humor || !answers.stress || !answers.motivation) {
      setErrorMessage('Proszę, wybierz jedną opcję w każdej kategorii!');
      return;
    }

    try {
      const response = await apiFetch('/api/survey', {
        method: 'POST',
        body: JSON.stringify(answers)
      });

      if (response.ok) {
  const wylosowanyCytat = await response.json(); 
  navigate('/dashboard', { state: { cytat: wylosowanyCytat } });
}
    } catch (error) {
      setErrorMessage('Błąd serwera. Sprawdź połączenie.');
    }
  };

  const renderEmojiButton = (category, value, emoji, label) => {
    const isSelected = answers[category] === value;

    return (
      <button
        type="button"
        onClick={() => handleSelect(category, value)}
        className={`flex flex-col items-center justify-center p-3 rounded-2xl transition-all duration-300 ${
          isSelected 
            ? 'bg-[#99CDD8] scale-110 shadow-lg ring-2 ring-[#657166]'
            : 'bg-[#FDE8D3] hover:bg-[#CFD6C4] hover:scale-105 opacity-80'
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

          
          <div className="flex flex-col gap-3">
            <h3 className="font-bold text-lg text-center">Poczucie humoru</h3>
            <div className="grid grid-cols-3 gap-4">
              {renderEmojiButton('humor', 'smutna', '😞', 'Słabo')}
              {renderEmojiButton('humor', 'neutralna', '😐', 'Neutralnie')}
              {renderEmojiButton('humor', 'wesola', '😄', 'Świetnie')}
            </div>
          </div>

         
          <div className="flex flex-col gap-3">
            <h3 className="font-bold text-lg text-center">Poziom stresu</h3>
            <div className="grid grid-cols-3 gap-4">
              {renderEmojiButton('stress', 'niski', '😌', 'Niski')}
              {renderEmojiButton('stress', 'sredni', '😬', 'Średni')}
              {renderEmojiButton('stress', 'wysoki', '🤯', 'Wysoki')}
            </div>
          </div>

         
          <div className="flex flex-col gap-3">
            <h3 className="font-bold text-lg text-center">Poziom motywacji</h3>
            <div className="grid grid-cols-3 gap-4">
              {renderEmojiButton('motivation', 'niska', '🥱', 'Niska')}
              {renderEmojiButton('motivation', 'srednia', '🤔', 'Średnia')}
              {renderEmojiButton('motivation', 'wysoka', '🚀', 'Wysoka')}
            </div>
          </div>

          
          {errorMessage && (
            <div className="text-red-500 text-sm font-bold text-center mt-2">
              {errorMessage}
            </div>
          )}

         
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
