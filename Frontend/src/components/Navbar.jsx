import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

/*
    Title: Navbar Component

    Purpose:
    The purpose of this component is to provide a navigation bar for the application.
    It includes links to different sections of the site, such as Home, Blog, Knowledge Base,
    and Account Portal. The navigation bar also handles user login/logout functionality.
*/

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
    <nav className="nav">
      <div className="nav-right">

        {!isLoggedIn ? (
          // If the user is not logged in, show links to Home, Login, and Register
          <>
            <Link to="/" className="nav-link">LegacyIQ</Link>
            <span className="nav-bar">|</span>
            <Link to="/login" className="nav-link">Login</Link>
            <span className="nav-bar">|</span>
            <Link to="/register" className="nav-link">Register</Link>
          </>
        ) : (
          // If the user is logged in, show links to Home, Blog, Knowledge Base, Account Portal, and Logout
          <>
            <Link to="/" className="nav-link">LegacyIQ</Link>
            <span className="nav-bar">|</span>
            <Link to="/blogs" className="nav-link">Blog</Link>
            <span className="nav-bar">|</span>
            <Link to="/account-portal" className="nav-link">Account</Link>
            <span className="nav-bar">|</span>
            <span onClick={handleLogout} className="nav-link">Logout</span>
            <span className="nav-bar">|</span>
          </>
        )}
      </div>
    </nav>
  );
}