import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Navbar({ isLoggedIn, setIsLoggedIn }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5000/account/logout', {
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
      <div style={styles.brand}>
        <span style={styles.logoText}>LegacyIQ</span>
        <i className="fi fi-bs-drafting-compass" style={styles.icon}></i>
      </div>

      <div style={styles.links}>
        {!isLoggedIn ? (
          <>
            <Link to="/" style={styles.link}>Home</Link>
            <Link to="/login" style={styles.link}>Login</Link>
            <Link to="/register" style={styles.link}>Register</Link>
          </>
        ) : (
          <>
            <Link to="/" style={styles.link}>Home</Link>
            <Link to="/blogs" style={styles.link}>Blog</Link>
            <Link to="/create" style={styles.link}>Create Blog</Link>
            <Link to="/knowledge-base" style={styles.link}>Knowledge Base</Link>
            <Link to="/account-portal" style={styles.link}>Account</Link>
            <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
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
    backgroundColor: '#333',
    padding: '10px 20px',
    color: 'white',
  },
  brand: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  logoText: {
    margin: 0,
    fontSize: '1.5rem',
    fontWeight: 'bold',
  },
  icon: {
    fontSize: '20px',
    color: 'white',
  },
  links: {
    display: 'flex',
    gap: '15px',
  },
  link: {
    color: 'white',
    textDecoration: 'none',
    fontWeight: 'bold',
  },
  logoutBtn: {
    backgroundColor: 'transparent',
    border: 'none',
    color: 'white',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
};
