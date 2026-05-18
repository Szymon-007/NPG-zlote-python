import { Link } from 'react-router-dom'

export default function Register() {
  return (
    <div className="p-10 text-center">
      <h1 className="text-3xl font-bold mb-4">Rejestracja</h1>
      <p className="mb-4 text-gray-400">Tu będzie formularz: Email, Hasło, Imię i Znak Zodiaku.</p>
      <Link to="/login" className="text-blue-500 hover:underline">
        Masz już konto? Zaloguj się
      </Link>
    </div>
  )
}