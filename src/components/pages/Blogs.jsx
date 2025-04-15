import React, { useState, useEffect } from 'react';
import './Home.css'; // Optional: Make sure Home.css styles exist

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://localhost:5000/blog/readposts', {
          method: 'GET',
          credentials: 'include',
        });

        if (response.ok) {
          const data = await response.json();
          if (Array.isArray(data) && data.length > 0) {
            setPosts(data);
            setMessage('');
          } else {
            setMessage('No posts available');
          }
        } else {
          setMessage('Failed to load posts');
          setPosts([]);
        }
      } catch (err) {
        console.error(err);
        setMessage('Error fetching posts');
        setPosts([]);
      }
    };

    fetchPosts();
  }, []);

  return (
    <div className="landing-page">
      
      {/* Section 6: Blog Post Feed */}
      <section className="blog-section">
        <h2>Latest Blog Posts</h2>
        {message && <p>{message}</p>}
        {!message && posts.length === 0 && <p>No posts available.</p>}

        {posts.length > 0 && (
          <div className="post-list">
            {posts.map((post, index) => (
              <div key={index} className="post">
                <h3>{post.title}</h3>
                <p>{post.content}</p>
                <small>{new Date(post.date).toLocaleDateString()}</small>
                <p>
                  <strong>Posted by:</strong> {post.firstName} {post.lastName}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>

    </div>
  );
}
