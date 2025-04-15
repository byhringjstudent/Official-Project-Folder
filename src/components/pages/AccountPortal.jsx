import React, { useEffect } from 'react'

export default function AccountPortal() {
    const [user, setUser] = React.useState(null);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState(null);

    useEffect(() => {
        const fetchAccountDetails = async () => {
          try {
            const response = await fetch("http://localhost:5000/account/viewAccountDetails"
                , { 
                    method: 'GET',
                    credentials: 'include', // Include credentials for session management
                });
            if (!response.ok) {
              throw new Error(`HTTP error: Status ${response.status}`);
            }
            const data = await response.json();
            setUser(data);
            setError(null);
          } catch (err) {
            setError(err.message);
            setUser(null);
          } finally {
            setLoading(false);
          }
        };
    
        fetchAccountDetails();
      }, []);
    
      if (loading) return <div>Loading account...</div>;
      if (error) return <div>Error: {error}</div>;
      if (!user) return <div>No user data found.</div>;
    
  return (
    <div className="container">
      <h2>Account Portal</h2>
      <p>Name:</p> {user.firstName} {user.lastName}
      <p>Email:</p> {user.email}
      <p>Verified:</p> {user.verifiedemail ? 'Yes' : 'No'}
    </div>
  )
}