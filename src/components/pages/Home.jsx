import React, { useState, useEffect } from 'react';

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://localhost:5000/blog/readposts', {
          method: 'GET',
          credentials: 'include', // Optional, if your app needs authentication
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Received posts:', data); // Log the data to check the response

          // Check if the data is an array and contains the expected fields
          if (Array.isArray(data) && data.length > 0) {
            setPosts(data); // Set the fetched posts into state
            setMessage(''); // Reset the message if posts are fetched successfully
          } else {
            setMessage('No posts available'); // Set a message if no posts are available
          }
        } else {
          setMessage('Failed to load posts'); // Set error message if response is not ok
          setPosts([]); // Clear posts if there's an error
        }
      } catch (err) {
        console.error(err);
        setMessage('Error fetching posts'); // Set error message for fetch failure
        setPosts([]); // Clear posts if there's an error
      }
    };

    fetchPosts();
  }, []); // Empty dependency array means this runs once when the component is mounted

  return (
    <div>
      {/* Welcome header */}
      <h1>Welcome to legacyIQ</h1>

      <h2>Here are all of the Blog Posts:</h2>

      {/* Display the error message if there's any */}
      {message && <p>{message}</p>}

      {/* If posts exist, render them */}
      {posts.length === 0 && !message && <p>No posts available.</p>}

      {posts.length > 0 && (
        <div>
          {posts.map((post, index) => (
            <div key={index} className="post">
              <h3>{post.title}</h3>
              <p>{post.content}</p>
              <small>{post.date}</small>
              <p><strong>Posted by:</strong> {post.firstName} {post.lastName} </p> {/* Display the poster's name */}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
