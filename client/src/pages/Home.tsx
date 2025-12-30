import { useNavigate } from 'react-router-dom'

export default function Home() {
  const navigate = useNavigate()
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      background: '#f8f9fa'
    }}>
      <h1 style={{ marginBottom: 32 }}>Bem-vindo ao KiloCal</h1>
      <button
        style={{
          width: 200,
          padding: 16,
          marginBottom: 16,
          fontSize: 18,
          borderRadius: 8,
          border: 'none',
          background: '#007bff',
          color: '#fff',
          cursor: 'pointer'
        }}
        onClick={() => navigate('/login')}
      >
        Login
      </button>
      <button
        style={{
          width: 200,
          padding: 16,
          fontSize: 18,
          borderRadius: 8,
          border: 'none',
          background: '#6c757d',
          color: '#fff',
          cursor: 'pointer'
        }}
        onClick={() => navigate('/register')}
      >
        Registrar
      </button>
    </div>
  )
}