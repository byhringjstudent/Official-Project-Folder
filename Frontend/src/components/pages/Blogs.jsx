import React, { useState, useEffect } from 'react';
import './AccountPortal.css'; 
import './Blogs.css'; 
import debounce from 'lodash.debounce';
import { useCallback } from 'react';


export default function Home() {
  const [posts, setPosts] = useState([]);
  const [status, setStatus] = useState('idle');
  const [query, setQuery] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false); // Add loading state


  // Function to fetch posts from the backend
  const fetchPosts = async (searchQuery) => {
    setLoading(true);
    setErrorMessage('');
    try {
      const response = await fetch(`http://localhost:5000/blog/search-published-post?q=${searchQuery}`, {
        method: 'GET',
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        if (data.status === 'success') {
          setPosts(data.post); // Set posts returned by the backend
          setStatus('success')
        } else {
          setPosts([]);
          setStatus('error')
          setErrorMessage(data.message || 'No posts found');
          
        }
      } else {
        setPosts([]);
        setStatus('error');
        setErrorMessage('Failed to load posts');
        
      }
    } catch (err) {
      console.error(err);
      setPosts([]);
      setStatus('error');
      setErrorMessage('Error fetching posts');
      
    }finally {
      setLoading(false);
    }
  };

  const debounceSearch = useCallback(
    debounce((query) => {
      fetchPosts(query);
    }, 800),
    []
  );

  const handleSearchChange = (e) => {
    setQuery(e.target.value);
  }

  // Effect to trigger fetching when the query changes
  useEffect(() => {
    if (query) {
      debounceSearch(query);
    } else {
      fetchPosts(''); // Fetch all posts if the query is empty
    }
  }, [query]); // Triggered when the query changes

  return (
    <div className="blog-list-container">
      {/* Section 6: Blog Post Feed */}
      <h2 style={{ textAlign: 'center', color: 'white', fontSize: '2rem'}}>Blog Posts</h2>
      <section className="blog-list">
        <input
          type="text"
          placeholder="Search Blog Posts"
          value={query}
          onChange={handleSearchChange} // Update query on user input
          className="all-search-bar"
        />
        
        {status === 'loading' && <p>Loading...</p>}

        {status === 'error' && <p>{errorMessage}</p>}

        {status === 'success' && posts.length === 0 && <p>No Posts Relate to Search.</p>}


        {status === 'success' && posts.length > 0 && (
  <div className="blog-list">
  {posts.map((post, index) => (
  <div key={index} className="all-user-blog-preview">
    <div className="post-content-list">
      <div className="post-text">
        <h3>{post.title}</h3>
        <p>{post.shortdescription}</p>
        <small>
          {post.tags.map((tag, index) => (
            <span key={index} className="tag-badge">
              {tag}
            </span>
          ))}
        </small>
        <p> </p>
        <small>{new Date(post.date).toLocaleDateString()}</small>
        <p>
          <strong>Posted by:</strong> {post.firstName} {post.lastName}
        </p>
        <a href={`/blog/${post.blogID}`}>Read more →</a>
      </div>

      {post.image_url && (
        <img
          src={`http://localhost:5000${post.image_url}`}
          alt="Blog Post"
          className="post-image-list"
        />
      )}
    </div>
  </div>
))}

  </div>
        )}
      </section>

      {/* Section 8: Footer */}
      <div class="blog-footer-wrapper">
         <footer class="blog-footer">
           © 2025 LegacyIQ · Privacy · For Support, Contact us at: {""}
          <a href="mailto:legacyiqdevteam@outlook.com">legacyiqdevteam@outlook.com</a>
        </footer>
     </div>
     </div>
  );
}
