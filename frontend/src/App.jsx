import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Survey from './pages/Survey'
import Dashboard from './pages/Dashboard'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
	<Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {/* Zabezpieczona Ankieta */}
        <Route path="/survey" element={
          <ProtectedRoute>
            <Survey />
          </ProtectedRoute>
        } />
        
        {/* Zabezpieczony Dashboard */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App