import { Link } from 'react-router-dom'

export default function Login() {
  return (
    <div className="p-10 text-center">
      <h1 className="text-3xl font-bold mb-4">Logowanie</h1>
      <p className="mb-4 text-gray-400">Tu będzie formularz: Email i Hasło.</p>
      <Link to="/register" className="text-blue-500 hover:underline">
        Nie masz konta? Zarejestruj się
      </Link>
    </div>
  )
}