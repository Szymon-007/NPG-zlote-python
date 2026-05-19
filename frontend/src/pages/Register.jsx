import { Link } from 'react-router-dom'

export default function Register() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#DAEBE3] p-4">
      
      <div className="bg-white p-10 rounded-2xl shadow-xl w-full max-w-md text-[#657166]">
        <h1 className="text-3xl font-bold text-center mb-8 !text-[#FDE8D3]">Rejestracja</h1>

        <form className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="Adres e-mail"
            className="w-full p-4 bg-[#FDE8D3] rounded-xl outline-none focus:ring-4 focus:ring-[#99CDD8]/50 text-[#657166] placeholder-[#657166]/60 transition-all font-medium"
          />
          <input
            type="password"
            placeholder="Hasło"
            className="w-full p-4 bg-[#FDE8D3] rounded-xl outline-none focus:ring-4 focus:ring-[#99CDD8]/50 text-[#657166] placeholder-[#657166]/60 transition-all font-medium"
          />
          <input
            type="text"
            placeholder="Twoje imię"
            className="w-full p-4 bg-[#FDE8D3] rounded-xl outline-none focus:ring-4 focus:ring-[#99CDD8]/50 text-[#657166] placeholder-[#657166]/60 transition-all font-medium"
          />

          {/* Kafelkowy Select dla znaku zodiaku */}
          <select
            className="w-full p-4 bg-[#FDE8D3] rounded-xl outline-none focus:ring-4 focus:ring-[#99CDD8]/50 text-[#657166] transition-all font-medium cursor-pointer"
            defaultValue=""
          >
            <option value="" disabled>Wybierz znak zodiaku</option>
            <option value="Baran">Baran</option>
            <option value="Byk">Byk</option>
            <option value="Bliźnięta">Bliźnięta</option>
            <option value="Rak">Rak</option>
            <option value="Lew">Lew</option>
            <option value="Panna">Panna</option>
            <option value="Waga">Waga</option>
            <option value="Skorpion">Skorpion</option>
            <option value="Strzelec">Strzelec</option>
            <option value="Koziorożec">Koziorożec</option>
            <option value="Wodnik">Wodnik</option>
            <option value="Ryby">Ryby</option>
          </select>

          {/* Zmieniony kolor przycisku dla urozmaicenia formularza */}
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
  )
}