import React, { useState, useEffect } from 'react';
import './Home.css'; // Optional: Make sure Home.css styles exist
import { Link } from 'react-router-dom';

/*
    Title: Home Component
    Purpose:
    The purpose of this component is to serve as the landing page for the application.
    It includes a hero banner, feature sections, testimonials, and a blog post feed.
    The component fetches the latest blog posts from the backend and displays them.
    It also provides a call to action for users to sign up.
*/

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [message, setMessage] = useState('');

  // Function to fetch posts from the backend
  // Note: The useEffect hook is used to fetch data when the component mounts.
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('/api/blog/read-latest-posts', {
          method: 'GET',
          credentials: 'include',
        });

        if (response.ok) {
          const data = await response.json();
          if (Array.isArray(data.posts) && data.posts.length > 0) {
            setPosts(data.posts);
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
      <h3 className="landing-header">Welcome To LegacyIQ</h3>
      {/* Section 1: Hero Banner */}
      <section className="hero-section">
        <h1>The World’s Most Intelligently Secure Estate Planning Platform</h1>
        <p>
          LegacyIQ combines AI with security to revolutionize your family's future.
        </p>
      </section>

      {/* Section 2: Feature Block with Image */}
      <section className="feature-section">
        <div className="feature-image">
          <img
            src="/assets/RAG%20image.png"
            alt="AI RAG Flow"
            width="300"
          />
        </div>
        <div className="feature-text">
          <h2>Revolutionize Your Estate Planning with AI</h2>
          <p>
            Our future AI engine helps automate and personalize your estate documents in minutes.
          </p>
        </div>
      </section>

      {/* Section 3: Vault / Security */}
      <section className="security-section">
        <img
          src="/assets/vault-icon.png"
          alt="Security Vault Icon"
          width="200"
        />
        <h3>Bank-Level Encryption & Document Vaults</h3>
        <p>
          Your trust documents are stored and managed with military-grade security.
        </p>
      </section>

      {/* Section 4: AI Agent Help Cards */}
      <section className="agent-section">
        <h2>In a Future Feature, Supercharge Your Planning with Our RAG Agent</h2>
        <div className="agent-cards">
          <div className="card">What documents do I need?</div>
          <div className="card">How do trusts compare to wills?</div>
          <div className="card">Who should I name as my executor?</div>
        </div>
      </section>

      {/* Section 5: Testimonials */}
      <section className="testimonials-section">
        <h2>What Our Users Say</h2>
        <blockquote>
          "LegacyIQ helped my family avoid thousands in probate — and it was easy to use!"
        </blockquote>
        <p>⭐⭐⭐⭐⭐</p>
      </section>

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
                <p>{post.shortdescription}</p>
                <small>
                  {post.tags.map((tag, index) => (
                    <span key={index} className="tag-badge">
                      {tag}
                    </span>
                  ))}
                </small>
                <p> </p>
                <div style={{ whiteSpace: 'pre-wrap' }}>
                  {post.content}
                </div>
                <small>{new Date(post.date).toLocaleDateString()}</small>
                <p>
                  <strong>Posted by:</strong> {post.firstName} {post.lastName}
                </p>

                {/* Display Image */}
                {post.image_url && (
                  <img
                    src={post.image_url} // Adjust the URL as needed
                    alt="Blog Post"
                    className="post-image"
                  />
                )}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Section 7: Call to Action */}
      <section className="cta-section">
        <h2>Start Your Free Trial Today</h2>
        <p>Join the community and experience the full power of AI-driven estate planning</p>
        <Link to="/register"><button>Sign Up</button></Link>
      </section>

      {/* Section 8: Footer */}
      <footer className="footer">
        <p>© 2025 LegacyIQ · Privacy · For Support, Contact us at: {""}
          <a href="mailto:legacyiqdevteam@outlook.com" className="text-blue-500 hover:underline">
          legacyiqdevteam@outlook.com
          </a>
        </p>
      </footer>
    </div>
  );
}
