import React from 'react';
import { Link, useNavigate } from 'react-router-dom';


export default function Navbar({ isLoggedIn, setIsLoggedIn }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5000/account/logout', {
        method: 'POST',
        credentials: 'include', // important for session cookies!
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
      <h2 style={styles.logo}>Legacy IQ</h2>
      <div style={styles.links}>
        {!isLoggedIn ? (
          <><Link to="/" style={styles.link}>Login</Link><Link to="/register" style={styles.link}>Register</Link></>
        ) : (
          <>
            <Link to="/home" style={styles.link}>Home</Link>
            <Link to="/create" style={styles.link}>Create Blog</Link>
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
  logo: {
    margin: 0,
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
