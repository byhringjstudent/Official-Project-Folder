import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './EditProfile.css'; // optional for styling

/*
    Title: EditAccount Component
    Purpose:
    The purpose of this component is to allow users to edit their account details.
    It includes a form for the user to enter their new first name, last name, and email address.
    Upon submission, it sends a request to the backend to update the user's account information.
*/

export default function EditAccount() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Handle form submission
  // This function is called when the user submits the form.
  // If the update is successful, it redirects the user to the account portal.
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // This function sends a PUT request to the backend API to update the user's account details.
    try {
      const response = await fetch('/api/account/edit', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ firstName, lastName, newEmail }),
      });

      const data = await response.json();
      setLoading(false);

      if (response.ok) {
        setMessage(data.message || "Account Successfully Updated");

        // After 1.5 seconds, redirect to home
        setTimeout(() => {
          navigate('/account-portal');
        }, 1500);
      } else {
        setMessage(data.message || 'Failed to update account details.');
      }
    } catch (error) {
      console.error('Error updating account:', error);
      setLoading(false);
      setMessage('Error connecting to server.');
    }
  };

  return (
    // Render the form for editing account details
    // The form includes fields for first name, last name, and email address.
    <div className="edit-account-container">
      {/* Form */}
      <form onSubmit={handleSubmit} className="edit-account-form">
        <h2>Edit Account Details</h2>

        <label htmlFor="firstName">New First Name</label>
        <input
          type="text"
          id="firstName"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          placeholder="Enter new first name"
        />

        <label htmlFor="lastName">New Last Name</label>
        <input
          type="text"
          id="lastName"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          placeholder="Enter new last name"
        />

        <label htmlFor="newEmail">New Email</label>
        <input
          type="email"
          id="newEmail"
          value={newEmail}
          onChange={(e) => setNewEmail(e.target.value)}
          placeholder="Enter new email"
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Updating...' : 'Update Details'}
        </button>

        {message && (
          <p className={`edit-account-message ${message.toLowerCase().includes('successfully') ? 'success' : 'error'}`}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
}
