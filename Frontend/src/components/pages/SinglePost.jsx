import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom'; // To get the post ID from the URL
import './SinglePost.css';
import './Home.css';

const SinglePost = () => {
  const { id } = useParams(); // Get the post ID from the URL
  const [post, setPost] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the post data from the backend
    const fetchPost = async () => {
      try {
        const response = await fetch(`/api/blog/get-single-post/${id}`, {
          method: 'GET',
          credentials: 'include', // Ensure cookies are sent with the request
        });
        if (!response.ok) {
          const data = await response.json();
          setError(data.message || 'Error retrieving post');
        } else {
          const data = await response.json();
          setPost(data.post[0]); // Assuming the response is in the format { post: [{...}] }
        }
      } catch (err) {
        setError('Error fetching data');
      }
    };

    fetchPost();
  }, [id]); // Refetch the data when the post ID changes

  const handleBackClick = () => {
    navigate(-1); 
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!post) {
    return <div>Loading...</div>;
  }

  return (
    <div className="single-post">
        
      {/* Displaying the single post */}
      <section className="single-blog">
  <div className="post">
    <h2>{post.title}</h2>
    <p>{post.shortdescription}</p>
    <small>
      {Array.isArray(post.tags)
        ? post.tags.map((tag, index) => (
            <span key={index} className="tag-badge">{tag}</span>
          ))
        : post.tags && post.tags.split(',').map((tag, index) => (
            <span key={index} className="tag-badge">{tag}</span>
          ))
      }
    </small>
    <p>{post.content}</p>
    <p>{new Date(post.date).toLocaleDateString()}</p>
    {post.image_url && (
      <img
        src={post.image_url}
        alt="Blog Post"
        className="post-image"
      />
    )}
  </div>

  {/* Button positioned at the bottom right */}
  <button className="back-button" onClick={handleBackClick}>
    ← Back
  </button>
</section>
      <div class="blog-footer-wrapper">
         <footer class="blog-footer">
           © 2025 LegacyIQ · Privacy · For Support, Contact us at: {""}
          <a href="mailto:legacyiqdevteam@outlook.com">legacyiqdevteam@outlook.com</a>
        </footer>
     </div>
    </div>
  );
};

export default SinglePost;