import { useState } from 'react'
import Login from './pages/Login'
import Home from './pages/Home'

function App() {
  const [user, setUser] = useState(null)
  const [showLogin, setShowLogin] = useState(false)

  if (showLogin) {
    return (
      <Login
        onLogin={(username) => { setUser(username); setShowLogin(false) }}
        onBack={() => setShowLogin(false)}
      />
    )
  }

  return (
    <Home
      user={user}
      onLoginClick={() => setShowLogin(true)}
      onLogout={() => setUser(null)}
    />
  )
}

export default App
