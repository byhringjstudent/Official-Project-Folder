import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Make sure this file exists in the same folder

/*

    Title: Login Component
    Purpose:        
    The purpose of this component is to handle the user login process.
    It includes a form for the user to enter their email and password,
    and it sends a request to the backend to authenticate the user.
    If the login is successful, it updates the application state to reflect that the user is logged in.

*/

export default function Login({ setIsLoggedIn }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/account/login', {
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

  // Render the form for user login 
  // The form includes fields for email and password, and a submit button.
  // When the form is submitted, it calls the handleSubmit function.
  return (
    <div className="login-container">
      {/* Form */}
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
