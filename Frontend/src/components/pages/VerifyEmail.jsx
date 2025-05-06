import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

/*
    Title: VerifyEmail Component
    Purpose:
    The purpose of this component is to handle the email verification process.

*/

export default function VerifyEmail() {
  const { token } = useParams(); // Capture token from URL
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState(''); // New state for success or error

  // Function to verify email using the token
  // This function will be called when the component mounts
  // It will send a request to the backend to verify the email
  // and update the message and status based on the response
  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const response = await fetch(`/api/verify_email/${token}`);
        const result = await response.json();
        setMessage(result.message || result.error);
        setStatus(response.ok ? 'success' : 'error');
      } catch (err) {
        setMessage('Verification failed. Please try again later.');
        setStatus('error');
        console.error(err);
      }
    };

    if (token) {
      verifyEmail();
    }
  }, [token]);

  return (
    // Render the verification message based on the status
    // If the status is success, show a success message
    <div style={styles.container}>
      <h2>Email Verification</h2>
      <div style={styles.messageBox(status)}>
        <p>{message}</p>
      </div>
      {status === 'error' && (
        <button onClick={() => window.location.href = "/"} style={styles.retryButton}>
          Go back to Home
        </button>
      )}
    </div>
  );
}

// Styles for the component
// These styles are used to style the container, message box, and button

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f4f4f4',
    minHeight: '100vh',
  },
  messageBox: (status) => ({
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center',
    maxWidth: '400px',
    marginTop: '20px',
    backgroundColor: status === 'success' ? '#d4edda' : '#f8d7da',
    color: status === 'success' ? '#155724' : '#721c24',
    border: `1px solid ${status === 'success' ? '#c3e6cb' : '#f5c6cb'}`,
  }),
  retryButton: {
    marginTop: '20px',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
};
