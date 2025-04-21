import React, { useState, useEffect } from 'react';
import './Home.css'; // Optional: Make sure Home.css styles exist

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://localhost:5000/blog/read-latest-posts', {
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
            Our AI engine helps automate and personalize your estate documents in minutes.
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
        <h2>Supercharge Your Planning with Our RAG Agent</h2>
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

      {/* Section 7: Call to Action */}
      <section className="cta-section">
        <h2>Start Your Free Trial Today</h2>
        <p>Experience the full power of AI-driven estate planning</p>
        <input type="email" placeholder="Enter your email" />
        <button>Sign Up</button>
      </section>

      {/* Section 8: Footer */}
      <footer className="footer">
        <p>© 2025 LegacyIQ · Privacy · Contact</p>
      </footer>
    </div>
  );
}
