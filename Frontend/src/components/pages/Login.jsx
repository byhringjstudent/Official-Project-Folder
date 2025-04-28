import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Make sure this file exists in the same folder

export default function Login({ setIsLoggedIn }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/account/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ email, password })
      });
    

      const data = await response.json();

      if (response.ok && data.message === 'User logged in successfully') {
        setMessage('Login successful! Redirecting...');
        setIsLoggedIn(true);
        localStorage.setItem('isLoggedIn', 'true');
        setTimeout(() => {
          navigate('/');
        }, 1500); // 1500 milliseconds = 1.5 seconds
      } else {
        setMessage(data.message || 'Login failed.');
      }
    } catch (error) {
      console.error('Login error:', error);
      setMessage('Error connecting to server.');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Login</h2>

        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Login</button>
        {message && (
          <p className={`login-message ${message.toLowerCase().includes('successfully') ? 'success' : 'error'}`}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
}
