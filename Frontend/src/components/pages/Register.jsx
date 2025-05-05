import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css'; // Make sure this file exists and is imported correctly

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = {
      email,
      password,
      firstName,
      lastName,
    };

    try {
      const response = await fetch('/api/account/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message || 'Registration successful!');
        localStorage.removeItem('isLoggedIn');
        sessionStorage.removeItem('isLoggedIn');
        document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;';
          setTimeout(() => {
            navigate('/');
          }, 1500); // 1500 milliseconds = 1.5 seconds
      } else {
        setMessage(data.message || 'Something went wrong.');
      }
    } catch (err) {
      console.error(err);
      setMessage('Server error, please try again later.');
    }
  };

  return (
    <div className="register-container">
      <form onSubmit={handleSubmit} className="register-form">
        <h2 className="form-title">Register</h2>
        
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        
        <label>First Name:</label>
        <input
          type="text"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          required
        />
        
        <label>Last Name:</label>
        <input
          type="text"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          required
        />
        
        <button type="submit">Register</button>
        <p className="form-message">{message}</p>
      </form>
    </div>
  );
}
