import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChangePassword.css'; // Make sure this file exists in the same folder

export default function Login({ setIsLoggedIn }) {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/account/updatePassword', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ currentPassword, newPassword })
      });
    

      const data = await response.json();

      if (response.ok && data.message === 'Password updated successfully') {
        setMessage('Password changed successfully!');

        setTimeout(() => {
          navigate('/account-portal');
        }, 1500); // 1500 milliseconds = 1.5 seconds
      } else {
        setMessage(data.message || 'Password change unsuccessful.');
      }
    } catch (error) {
      console.error('Changing password error:', error);
      setMessage('Error connecting to server.');
    }
  };

  return (
    <div className="edit-password-container">
      <form onSubmit={handleSubmit} className="edit-password-form">
        <h2>Change Password</h2>

        <label htmlFor="currentPassword">Current Password</label>
        <input
          type="password"
          id="currentPassword"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          required
        />

        <label htmlFor="newPassword">New Password:</label>
        <input
          type="password"
          id="newPassword"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />

        <button type="submit">Change Password</button>

        <p className={`edit-password-message ${message.includes('successfully') ? 'success' : ''}`}>
        {message}
        </p>

      </form>
    </div>
  );
}
