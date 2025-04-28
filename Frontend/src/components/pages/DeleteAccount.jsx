import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './DeleteAccount.css';  // Make sure to import the CSS file

const DeleteAccount = () => {
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleDeleteAccount = async (e)    => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const response = await fetch('/account/deleteAccount', {
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
