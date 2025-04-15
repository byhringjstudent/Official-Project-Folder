import React, { useEffect, useState } from 'react';
import './AccountPortal.css'; // Adjusted to reflect the correct relative path

const AccountPortal = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAccountDetails = async () => {
      try {
        const response = await fetch("http://localhost:5000/account/viewAccountDetails", {
          method: 'GET',
          credentials: 'include', // For cookies/session
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
    <div className="account-page">
      <aside className="sidebar">
        <div className="logo">🌿 LegacyIQ</div>
        <input type="text" placeholder="Search" className="search-bar" />
        <nav className="menu">
          <h4>Dashboard</h4>
          <ul>
            <li><a href="/blogs">📝 Blogs</a></li>
            <li><a href="/notifications">🔔 Notifications</a></li>
            <li><a href="/write">✍️ Write</a></li>
          </ul>
          <h4>Settings</h4>
          <ul>
            <li><a href="/edit-profile">👤 Edit Profile</a></li>
            <li><a href="/change-password">🔒 Change Password</a></li>
          </ul>
        </nav>
      </aside>

      <main className="account-content">
        <h2>Welcome to your Account Portal</h2>
        <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Verified:</strong> {user.verifiedemail ? 'Yes' : 'No'}</p>
      </main>
    </div>
  );
};

export default AccountPortal;


