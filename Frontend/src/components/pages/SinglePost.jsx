import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom'; // To get the post ID from the URL
import './SinglePost.css';

const SinglePost = () => {
  const { id } = useParams(); // Get the post ID from the URL
  const [post, setPost] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the post data from the backend
    const fetchPost = async () => {
      try {
        const response = await fetch(`http://localhost:5000/blog/get-single-post/${id}`, {
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
        
    <button className="back-button" onClick={handleBackClick}>Back</button>
      {/* Displaying the single post */}
      <section className="single-blog">
        {/* Display error message if provided */}
        {error && <p>{error}</p>}

        {/* Render the post details */}
        <div className="post">
          <h2>{post.title}</h2>
          <p>{post.shortdescription}</p>
          <small>
            {/* If tags is an array, map through it */}
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
          <small>{new Date(post.date).toLocaleDateString()}</small>

          {/* Display Image */}
          {post.image_url && (
                  <img
                    src={`http://localhost:5000${post.image_url}`} // Adjust the URL as needed
                    alt="Blog Post"
                    className="post-image"
                  />
        )}
        </div>
      </section>
    </div>
  );
};

export default SinglePost;