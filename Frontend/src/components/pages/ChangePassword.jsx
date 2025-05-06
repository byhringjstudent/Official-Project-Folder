import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChangePassword.css'; // Make sure this file exists in the same folder

/*
    Title: ChangePassword Component
    Purpose:        
    The purpose of this component is to handle the user password change process.
    It includes a form for the user to enter their current password and new password,
    and it sends a request to the backend to update the user's password.
    If the password change is successful, it redirects the user to the account portal.
*/

export default function Login({ setIsLoggedIn }) {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  // Handle form submission
  // This function is called when the user submits the form.
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate password length
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

      // Check if the response is ok and if the message indicates success
      // If the password change is successful, redirect to the account portal
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
    // Render the form for changing the password
    <div className="edit-password-container">
      <form onSubmit={handleSubmit} className="edit-password-form">
        <h2>Change Password</h2>

        {/* Input fields for current and new password */}
        <label htmlFor="currentPassword">Current Password</label>
        <input
          type="password"
          id="currentPassword"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          required
        />

        {/* New password input field */}
        <label htmlFor="newPassword">New Password:</label>
        <input
          type="password"
          id="newPassword"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />

        <button type="submit">Change Password</button>

        {/* Display message after form submission */}
        <p className={`edit-password-message ${message.includes('successfully') ? 'success' : ''}`}>
        {message}
        </p>

      </form>
    </div>
  );
}
