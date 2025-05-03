import React, { useEffect, useState } from 'react';
import './AccountPortal.css';
import { useNavigate } from 'react-router-dom';

const AccountPortal = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
    const fetchAccountDetails = async () => {
      try {
        const response = await fetch("http://localhost:5000/account/viewAccountDetails", {
          method: 'GET',
          credentials: 'include',
        });
        if (!response.ok) throw new Error(`Status ${response.status}`);
        const data = await response.json();
        setUser(data);
      } catch (err) {
        setError(err.message);
      }
    };

      

    const fetchUserBlogs = async () => {
      try {
        const response = await fetch("http://localhost:5000/account/blog-posts", {
          method: 'GET',
          credentials: 'include',
        });
        if (!response.ok) throw new Error(`Status ${response.status}`);
        const data = await response.json();
        setBlogs(data.blogs);
      } catch (err) {
        console.error("Error fetching blogs:", err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAccountDetails();
    fetchUserBlogs();
  }, []);



  const deleteBlog = async (blogID) => {
    const response = await fetch(`http://localhost:5000/blog/deleteposts/${blogID}`, {
      method: 'DELETE', // DELETE method
      headers: {
        'Content-Type': 'application/json',
      },
    });

  
    if (response.ok) {
      // Remove the blog from the UI after deletion
      setBlogs(blogs.filter(blog => blog.blogID !== blogID));
      alert('Blog deleted successfully!');
    } else {
      const data = await response.json();
      alert(data.message || 'Failed to delete post');
    }
  };
  
  

  const editBlog = async (blogID) => {
    const response = await fetch(`http://localhost:5000/blog/updateposts/${blogID}`, {
      method: 'PUT', // Use PUT or PATCH for updating
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title, content, shortDesc, tags, status }),
    });
  
    if (response.ok) {
      alert('Blog edited successfully!');
    } else {
      const data = await response.json();
      alert(data.message || 'Failed to edit post');
    }
  };


  if (loading) return <div>Loading account...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>No user data found.</div>;

  return (
    <div className="account-page">
      <aside className="sidebar">
        <div className="logo">🌿 LegacyIQ</div>
        <input type="text" placeholder="Search" className="search-bar" />
        <nav className="menu">
          <h4>Dashboard</h4>
          <ul>
            <li><a href="/blogs">📝 Blogs</a></li>
            <li><a href="/write">✍️ Write</a></li>
          </ul>
          <h4>Settings</h4>
          <ul>
            <li><a href="/edit-profile">👤 Edit Profile</a></li>
            <li><a href="/change-password">🔒 Change Password</a></li>
            <li><a href="/account-deletion">❌ Delete Account</a></li>
          </ul>
          <h4>Need Help? Email Support at:</h4>
          <a href="mailto:legacyiqdevteam@outlook.com" className="text-blue-500 hover:underline">
          ✉️ legacyiqdevteam@outlook.com
          </a>
          <p></p>
          <h5>© 2025 LegacyIQ</h5>
        </nav>
      </aside>
  
      <main className="account-content">
        <h2>Welcome to your Account Portal</h2>
        <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Verified:</strong> {user.verifiedemail ? '✅ Yes' : ' ❌ No'}</p>
  
        <hr />
  
        <h3>Your Blog Posts</h3>
        {blogs.length === 0 ? (
          <p>No blog posts yet.</p>
        ) : (
          blogs.map((blog) => (
            <div key={blog.blogID} className="user-blog-preview">
              <h4>{blog.title}</h4>
              <p className={`blog-status ${blog.status === 'published' ? 'published' : 'draft'}`}>
                {blog.status === 'published' ? 'Published' : 'Draft'}
              </p>
              <p>{blog.shortdescription}</p>
              <small>{new Date(blog.date).toLocaleDateString()}</small>
              <p></p>
              <a href={`/blog/${blog.blogID}`}>Read more →</a>
              <div className = "button-group">
              <button onClick={() => navigate(`/edit-post/${blog.blogID}`)} className="edit-button">
                Edit
              </button>
              <button onClick={() => deleteBlog(blog.blogID)} className="delete-button">
                Delete
              </button>
              </div>
            </div>
          ))
        )}
      </main>
    </div>
    
  )};

export default AccountPortal;

