import React, { useEffect, useState } from 'react';
import './AccountPortal.css';
import { useNavigate } from 'react-router-dom';




const AccountPortal = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // New blog state
  const [title, setTitle] = useState('');
  const [shortDesc, setShortDesc] = useState('');
  const [tagInput, setTagInput] = useState('');
  const [tags, setTags] = useState([]);
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

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
        setBlogs(data);
      } catch (err) {
        console.error("Error fetching blogs:", err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAccountDetails();
    fetchUserBlogs();
  }, []);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setImagePreview(URL.createObjectURL(file));
  };

  const handleAddTag = (e) => {
    if (e.key === 'Enter' && tagInput.trim() && tags.length < 10) {
      setTags([...tags, tagInput.trim()]);
      setTagInput('');
    }
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('shortDescription', shortDesc);
    formData.append('tags', JSON.stringify(tags));
    formData.append('image', image);

    try {
      const response = await fetch('http://localhost:5000/blog/create', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });

      if (!response.ok) throw new Error('Blog creation failed');

      alert('Blog published successfully!');
      setTitle('');
      setShortDesc('');
      setTags([]);
      setTagInput('');
      setImage(null);
      setImagePreview(null);
    } catch (err) {
      alert('Error: ' + err.message);
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
            <li><a href="/notifications">🔔 Notifications</a></li>
            <li><a href="/write">✍️ Write</a></li>
          </ul>
          <h4>Settings</h4>
          <ul>
            <li><a href="/edit-profile">👤 Edit Profile</a></li>
            <li><a href="/change-password">🔒 Change Password</a></li>
          </ul>
        </nav>
      </aside>

      <main className="account-content">
        <h2>Welcome to your Account Portal</h2>
        <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Verified:</strong> {user.verifiedemail ? 'Yes' : 'No'}</p>

        <hr style={{ margin: '2rem 0' }} />

        <h3>Your Blog Posts</h3>
        {blogs.length === 0 ? (
          <p></p>
        ) : (
          blogs.map((blog) => (
            <div key={blog.id} className="user-blog-preview">
              <h4>{blog.title}</h4>
              <p>{blog.shortDescription}</p>
              <a href={`/blog/${blog.id}`}>Read more →</a>
              <hr />
            </div>
          ))
        )}

        <hr style={{ margin: '3rem 0 1rem' }} />
        <h3>Create New Blog</h3>

        {/* Preview Section */}
        {imagePreview && (
          <img src={imagePreview} alt="Preview" className="preview-image" />
        )}
        <h4>{title || 'Your Blog Title'}</h4>
        <p>{shortDesc || 'Your short description will appear here.'}</p>

        {/* Blog Form */}
        <input
          type="text"
          placeholder="Blog Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <textarea
          placeholder="Short Description about your post"
          value={shortDesc}
          onChange={(e) => setShortDesc(e.target.value)}
          maxLength={150}
        />

        <input
          type="text"
          placeholder="Enter topic and press Enter"
          value={tagInput}
          onChange={(e) => setTagInput(e.target.value)}
          onKeyDown={handleAddTag}
        />

        <div className="tag-list">
          {tags.map((tag, i) => (
            <span key={i} className="tag-chip">{tag}</span>
          ))}
        </div>

        <input type="file" accept="image/*" onChange={handleImageChange} />

        <button onClick={handleSubmit} className="publish-button">Publish</button>
      </main>
    </div>
  );
};



export default AccountPortal;