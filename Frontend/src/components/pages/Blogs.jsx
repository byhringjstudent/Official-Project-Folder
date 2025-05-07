import React, { useState, useEffect } from 'react';
import './AccountPortal.css'; 
import './Blogs.css'; 
import debounce from 'lodash.debounce';
import { useCallback } from 'react';

/*
    Title: Blog Component
    Purpose:      
    The purpose of this component is to display a list of blog posts with
    functionality to search individual posts. It allows users view those blogs
    and provides a link to read more about each blog post.
    
*/


export default function Home() {
  const [posts, setPosts] = useState([]);
  const [status, setStatus] = useState('idle');
  const [query, setQuery] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [allPosts, setAllPosts] = useState([]);
  const [filteredPosts, setFilteredPosts] = useState([]);
  const [loading, setLoading] = useState(false); // Add loading state


  // Function to fetch posts from the backend
  const fetchPosts = async (searchQuery) => {
    setLoading(true);
    setErrorMessage('');
    try {
      const response = await fetch(`/api/blog/search-published-post`, {
        method: 'GET',
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        if (data.status === 'success') {
          setAllPosts(data.post); // Set posts returned by the backend
          setFilteredPosts(data.post); // Set filtered posts to all posts initially
          setStatus('success')
        } else {
          setAllPosts([]);
          setFilteredPosts([]); // Clear filtered posts if no posts found
          setStatus('error')
          setErrorMessage(data.message || 'No posts found');
          
        }
      } else {
        setAllPosts([]);
        setFilteredPosts([]);
        setStatus('error');
        setErrorMessage('Failed to load posts');
        
      }
    } catch (err) {
      // Handle error fetching posts
      console.error(err);
      setAllPosts([]);
      setFilteredPosts([]);
      setStatus('error');
      setErrorMessage('Error fetching posts');
      
    }finally {
      setLoading(false);
    }
  };
  


  // Debounced search function to filter posts based on user input
  // This function will be called after the user stops typing for 300ms
  const debounceSearch = useCallback(
    debounce((searchVal) => {
      const words = searchVal.toLowerCase().trim().split(/[\s+,]/).filter(Boolean); // Split by whitespace
      const filtered = allPosts.filter(post =>
        words.every(word =>
          post.title.toLowerCase().includes(word) ||
          post.shortdescription.toLowerCase().includes(word) ||
          post.firstName.toLowerCase().includes(word) ||
          post.lastName.toLowerCase().includes(word) ||
          (post.tags && post.tags.some(tag => tag.toLowerCase().includes(word)))
        )
      );
      setFilteredPosts(filtered);
    }, 300),
    [allPosts]
  );

  // Effect to clean up the debounce function on unmount
  const handleSearchChange = (e) => {
    const newQuery = e.target.value;
    setQuery(newQuery);
    debounceSearch(newQuery);
  };

  // Effect to trigger fetching when the query changes
  useEffect(() => {
    fetchPosts(); // Initial fetch
  }, []);

  return (
    <div className="blog-list-container">
      {/* Header */}
      <h2 style={{ textAlign: 'center', color: 'white', fontSize: '2rem'}}>Blog Posts</h2>
      <section className="blog-list">
        <input
          type="text"
          placeholder="Search Blog Posts"
          value={query}
          onChange={handleSearchChange} // Update query on user input
          className="all-search-bar"
        />
        {/* Display loading state  */}
        {status === 'loading' && <p>Loading...</p>}
        {/* // Display error message if any */}
        {status === 'error' && <p>{errorMessage}</p>}
        {/* // Display message if no posts found */}
        {status === 'success' && filteredPosts.length === 0 && <p>No Posts Relate to Search.</p>}
        {/* // Display posts if available */}
        {status === 'success' && filteredPosts.length > 0 && (
  <div className="blog-list">
  {/* // Map through the filtered posts and display them */}
  {filteredPosts.map((post, index) => (
  <div key={index} className="all-user-blog-preview">
    <div className="post-content-list">
      <div className="post-text">
        {/* // Display the title and short description of the post */}
        <h3>{post.title}</h3>
        <p>{post.shortdescription}</p>
        <small>
          {/* // Display the tags associated with the post */}
          {post.tags.map((tag, index) => (
            <span key={index} className="tag-badge">
              {tag}
            </span>
          ))}
        </small>
        <p> </p>
        {/* // Display the date in a more readable forma */}
        <small>{new Date(post.date).toLocaleDateString()}</small>
        <p>
          {/* // Display the author of the post */}
          <strong>Posted by:</strong> {post.firstName} {post.lastName}
        </p>
        {/* // Display a button to read more about the post */}
        <a href={`/blog/${post.blogID}`}>Read more →</a>
      </div>

      {/* // Display the image if it exists */}
      {post.image_url && (
        <img
          src={post.image_url}
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

      {/* Footer */}
      <div class="blog-footer-wrapper">
         <footer class="blog-footer">
           © 2025 LegacyIQ · Privacy · For Support, Contact us at: {""}
          <a href="mailto:legacyiqdevteam@outlook.com">legacyiqdevteam@outlook.com</a>
        </footer>
     </div>
     </div>
  );
}
