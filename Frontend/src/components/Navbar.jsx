import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Navbar({ isLoggedIn, setIsLoggedIn }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch('/api/account/logout', {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        console.log('Logged out successfully');
        localStorage.removeItem('isLoggedIn');
        setIsLoggedIn(false);
        navigate('/');
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  return (
    <nav style={styles.nav}>
      {/* Right side: Ordered links with bars */}
      <div style={styles.right}>
        {!isLoggedIn ? (
          <>
            <Link to="/" style={styles.link}>LegacyIQ</Link>
            <span style={styles.bar}>|</span>
            <Link to="/login" style={styles.link}>Login</Link>
            <span style={styles.bar}>|</span>
            <Link to="/register" style={styles.link}>Register</Link>
          </>
        ) : (
          <>
            <Link to="/" style={styles.link}>LegacyIQ</Link>
            <span style={styles.bar}>|</span>
            <Link to="/blogs" style={styles.link}>Blog</Link>
            <span style={styles.bar}>|</span>
            <Link to="/knowledge-base" style={styles.link}>Knowledge Base</Link>
            <span style={styles.bar}>|</span>
            <Link to="/account-portal" style={styles.link}>Account</Link>
            <span style={styles.bar}>|</span>
            <span onClick={handleLogout} style={styles.link}>Logout</span>
            <span style={styles.bar}>|</span>
          </>
        )}
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#2C3E50',
    padding: '10px 20px',
    color: 'white',
    borderBottom: '4px solid #F1C40F',
  },
  right: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    flexWrap: 'wrap',
  },
  link: {
    color: 'white',
    textDecoration: 'none',
    fontWeight: 'bold',
    fontSize: '1rem',
    cursor: 'pointer',
    padding: '0 6px',
  },
  bar: {
    color: '#F1C40F',
    fontWeight: 'bold',
  },
};
