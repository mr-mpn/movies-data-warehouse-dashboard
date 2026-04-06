import { useState } from 'react'
import './Login.css'

const API_URL = import.meta.env.VITE_API_URL

function Login({ onLogin, onBack }) {
  const [isSignUp, setIsSignUp] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    const endpoint = isSignUp ? '/auth/sign_up' : '/auth/log_in'

    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong')
      }

      if (isSignUp) {
        setIsSignUp(false)
        setError(null)
        setUsername('')
        setPassword('')
        alert('Account created. Please sign in.')
      } else {
        onLogin(username)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <nav className="login-navbar">
        <div className="login-navbar-brand">MoviesDash</div>
      </nav>

      <div className="login-container">
        <div className="login-card">
          <h1>{isSignUp ? 'Create Account' : 'Sign In'}</h1>
          <p className="login-subtitle">
            {isSignUp ? 'Sign up to access all features' : 'Welcome back'}
          </p>

          <form onSubmit={handleSubmit}>
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {error && <div className="login-error">{error}</div>}

            <button type="submit" disabled={loading}>
              {loading ? 'Please wait...' : isSignUp ? 'Sign Up' : 'Sign In'}
            </button>
          </form>

          <p className="login-toggle">
            {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
            <button
              type="button"
              className="toggle-btn"
              onClick={() => { setIsSignUp(!isSignUp); setError(null) }}
            >
              {isSignUp ? 'Sign In' : 'Sign Up'}
            </button>
          </p>
          <p className="login-toggle">
            <button type="button" className="toggle-btn" onClick={onBack}>
              Back to Dashboard
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login
