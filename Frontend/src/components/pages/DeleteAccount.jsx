import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './DeleteAccount.css';  // Make sure to import the CSS file


/*
    Title: DeleteAccount Component

    Purpose:
    The purpose of this component is to provide a user interface for deleting a user account.
    It includes a form where the user can enter their password to confirm the deletion.
    Upon submission, it sends a request to the backend to delete the account.
    If successful, it redirects the user to the home page.
*/

const DeleteAccount = () => {
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    // This function is called when the user submits the form. 
    // It sends a request to the backend to delete the account.
    const handleDeleteAccount = async (e)    => {
        e.preventDefault();
        setIsLoading(true);

        
        try {
            const response = await fetch('/api/account/deleteAccount', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ password }),
            });

            const data = await response.json();

            if (response.ok) {
                setMessage(data.message);
                setTimeout(() => {
                    navigate('/');
                  }, 1500);
            } else {
                setMessage(data.message);
            }
        } catch (error) {
            setMessage('Error deleting account: ' + error.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        // Render the form for deleting the account
        // The form includes a password field and a submit button.
        // When the form is submitted, it calls the handleDeleteAccount function.
        // The message state is used to display success or error messages.
        <div className="delete-account-container">
            <form className="delete-account-form" onSubmit={handleDeleteAccount}>
                <h2>Delete Your Account</h2>
                <p>Confirm Password to Delete Account</p>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Deleting...' : 'Delete Account'}
                </button>
                {message && (
                    <div className={`delete-account-message ${message.includes('success') ? 'success' : 'error'}`}>
                        {message}
                    </div>
                )}
            </form>
        </div>
    );
};

export default DeleteAccount;
