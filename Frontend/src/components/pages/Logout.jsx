import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = ({ setIsLoggedIn }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const logout = async () => {
      try {
        // Send request to backend to clear session
        const response = await fetch('/api/account/logout', {
          method: 'POST',
          credentials: 'include', // Make sure to include credentials (cookies)
        });

        const data = await response.json();
        if (data.message === 'User logged out successfully') {
          // Clear localStorage or sessionStorage (if used)
          localStorage.removeItem('isLoggedIn'); // or sessionStorage.removeItem('isLoggedIn');
          sessionStorage.removeItem('isLoggedIn');
          document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;';
          setIsLoggedIn(false);  // Update state to reflect user is logged out

          // Redirect user to login page
          navigate('/');
        } else {
          alert(data.message); // Handle any error message from the backend
        }
      } catch (err) {
        console.error(err);
        alert('Logout failed');
      }
    };

    logout();
  }, [navigate, setIsLoggedIn]);

  return (
    <div>Logging you out...</div>  // Optionally show a message while logging out
  );
};

export default Logout;