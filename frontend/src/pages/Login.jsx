import { Link } from 'react-router-dom'

export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#DAEBE3] p-4">
      
      <div className="bg-white p-10 rounded-2xl shadow-xl w-full max-w-md text-[#657166]">
        {/* Zmieniony kolor tekstu nagłówka */}
        <h1 className="text-3xl font-bold text-center mb-8 !text-[#FDE8D3]">Zaloguj się</h1>

        <form className="flex flex-col gap-5">
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
  )
}