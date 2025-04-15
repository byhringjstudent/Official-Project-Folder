import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './components/pages/Login';
import Home from './components/pages/Home';
import CreatePost from './components/CreatePost';
import Register from './components/pages/Register';
import Logout from './components/pages/Logout';  // Import Logout component
import KnowledgeBase from './components/pages/KnowledgeBase';
import VerifyEmail from './components/pages/VerifyEmail';
import AccountPortal from './components/pages/AccountPortal';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);  // State to track if the user is logged in
  const navigate = useNavigate();

  // Check login status when the app loads
  useEffect(() => {
    const verifySession = async () => {
      try {
        const res = await fetch('http://localhost:5000/account/check-auth', {
          credentials: 'include',
        });
  
        if (res.ok) {
          setIsLoggedIn(true);  // Set to true if the response is ok
          localStorage.setItem('isLoggedIn', 'true');  // Store login status
        } else {
          setIsLoggedIn(false);  // Set to false if not ok
          localStorage.removeItem('isLoggedIn');  // Remove login status
          if (window.location.pathname !== '/' && window.location.pathname !== '/register') {
            navigate('/');  // Redirect to login
          }
        }
      } catch (error) {
        console.error('Error verifying session:', error);
        setIsLoggedIn(false);
        localStorage.removeItem('isLoggedIn');
        if (window.location.pathname !== '/' && window.location.pathname !== '/register') {
          navigate('/');
        }
      }
    };
  
    verifySession(); // Run the check on mount
  }, [navigate]);
  

  return (
    <>
      <Navbar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />  {/* Pass down isLoggedIn to Navbar */}
      <Routes>
        {/* Login Route */}
        <Route
          path="/"
          element={<Login setIsLoggedIn={(val) => {
            setIsLoggedIn(val);  // Update state when logged in or logged out
            localStorage.setItem('isLoggedIn', val);  // Store login status in localStorage
          }} />}
        />
        <Route path="/register" element={<Register />} />
        {/* Only show these routes if logged in */}
        {isLoggedIn && (
          <>
            <Route path="/home" element={<Home />} />
            <Route path="/create" element={<CreatePost />} />
          </>
        )}
        {/* Logout Route */}
        <Route
          path="/logout"
          element={<Logout setIsLoggedIn={setIsLoggedIn} />}
        />
        {/* Knowledge Base Route */}
        <Route path="/knowledge-base" element={<KnowledgeBase />} />
        {/* Redirect to home if no match */}

         {/* Email Verification Route */}
         <Route path="/verify-email" element={<VerifyEmail />} />

         <Route path='/account-portal' element={<AccountPortal />} />

      </Routes>
    </>
  );
}

export default App;

