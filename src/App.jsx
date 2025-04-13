import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './components/pages/Login';
import Home from './components/pages/Home';
import CreatePost from './components/CreatePost';
import Register from './components/pages/Register';
import Logout from './components/pages/Logout';  // Import Logout component

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);  // State to track if the user is logged in
  const navigate = useNavigate();

  // Check login status when the app loads
  useEffect(() => {
    const loggedInStatus = localStorage.getItem('isLoggedIn') === 'true';  // Retrieve login status from localStorage
    setIsLoggedIn(loggedInStatus);  // Update the state based on the stored status
  }, []);

  // Redirect to login page if not logged in
  useEffect(() => {
    const currentPath = window.location.pathname;
    if (!isLoggedIn && currentPath !== '/' && currentPath !== '/register') {
      navigate('/');
    }
  }, [isLoggedIn, navigate]);
  

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
      </Routes>
    </>
  );
}

export default App;

