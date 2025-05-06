import React, { useEffect, useState } from 'react';
import './AccountPortal.css';
import { useNavigate } from 'react-router-dom';
import BlogList from '../UserBlogList';

/* 	    
        Title: Account Portal Component
        
        Purpose:

        The purpose of this component is to provide a user account portal 
        where users can view their account details and manage their blog posts.
        It includes functionality to fetch user data, display blog posts, and 
        allow users to delete or edit their blogs.
*/


const AccountPortal = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState("");

  // Fetch user and blog data on mount
  // Note: The useEffect hook is used to fetch data when the component mounts.
  // It fetches account details and user blogs from the backend API.
  useEffect(() => {
    const fetchAccountDetails = async () => {
      try {
        const response = await fetch("/api/account/viewAccountDetails", {
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

    // Fetch user blogs
    // Note: This function is called after the account details are fetched
    // to ensure the user is logged in before fetching blogs.
    const fetchUserBlogs = async () => {
      try {
        const response = await fetch("/api/account/blog-posts", {
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

  // Handle blog deletion
  // Note: This function is called when the user clicks the delete button on a blog post.
  // It sends a DELETE request to the backend API to remove the blog post.
  const deleteBlog = async (blogID) => {
    const response = await fetch(`/api/blog/deleteposts/${blogID}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      setBlogs(blogs.filter(blog => blog.blogID !== blogID));
      alert('Blog deleted successfully!');
    } else {
      const data = await response.json();
      alert(data.message || 'Failed to delete post');
    }
  };

  // Handle blog editing (note: missing local variables like title, content, etc.)
  const editBlog = async (blogID) => {
    // You may want to pass values or open an edit modal
    const response = await fetch(`/api/blog/updateposts/${blogID}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title, content, shortDesc, tags, status }), // Ensure these are defined
    });

    if (response.ok) {
      alert('Blog edited successfully!');
    } else {
      const data = await response.json();
      alert(data.message || 'Failed to edit post');
    }
  };

  // Handle loading, error, or no user state
  if (loading) return <div>Loading account...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>No user data found.</div>;

  return (
    <div className="account-page">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">🌿 LegacyIQ</div>

        <nav className="menu">
          <div className="menu-content">
            {/* Dashboard Links */}
            <h4>Dashboard</h4>
            <ul>
              <li><a href="/blogs">📝 Blogs</a></li>
              <li><a href="/write">✍️ Write</a></li>
            </ul>

            {/* Settings Links */}
            <h4>Settings</h4>
            <ul>
              <li><a href="/edit-profile">👤 Edit Profile</a></li>
              <li><a href="/change-password">🔒 Change Password</a></li>
              <li><a href="/account-deletion">❌ Delete Account</a></li>
            </ul>
          </div>

          {/* Sidebar Footer */}
          <div className="sidebar-footer">
            <h4>Need Help? Email Support at:</h4>
            <a href="mailto:legacyiqdevteam@outlook.com" className="text-blue-500 hover:underline">
              ✉️ legacyiqdevteam@outlook.com
            </a>
            <h5>© 2025 LegacyIQ</h5>
          </div>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="account-content">
        <h2>Welcome to your Account Portal</h2>
        <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Verified:</strong> {user.verifiedemail ? '✅ Yes' : '❌ No'}</p>

        <hr />

        {/* Blog Posts Section */}
        <h3>Your Blog Posts</h3>
        {blogs.length === 0 ? (
          <p>No blog posts yet.</p>
        ) : (
          <BlogList
            blogs={blogs}
            deleteBlog={deleteBlog}
            editBlog={editBlog}
            query={query}
            setQuery={setQuery}
          />
        )}
      </main>
    </div>
  );
};

export default AccountPortal;
