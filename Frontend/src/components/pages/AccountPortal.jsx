import React, { useEffect, useState } from 'react';
import './AccountPortal.css';
import { useNavigate } from 'react-router-dom';

const AccountPortal = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [shortDesc, setShortDesc] = useState('');
  const [tagInput, setTagInput] = useState('');
  const [status, setStatus] = useState('draft');
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

  const resetForm = () => {
    setTitle('');
    setContent('');
    setShortDesc('');
    setTags([]);
    setTagInput('');
    setImage(null);
    setImagePreview(null);
  };

  const handleSubmit = async (status) => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('content', content);
    formData.append('shortDescription', shortDesc);
    formData.append('tags', JSON.stringify(tags));
    formData.append('image', image);
    formData.append('status', status)

    try {
      const response = await fetch('http://localhost:5000/blog/createposts', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });

      if (!response.ok) throw new Error('Blog creation failed');
      alert('Blog published successfully!');
      resetForm();
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const handleSaveDraft = () => {
    handleSubmit('draft'); // Call handleSubmit with 'draft'
  };
  
  const handlePublish = () => {
    handleSubmit('published'); // Call handleSubmit with 'publish'
  };

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
    } else {
      const data = await response.json();
      alert(data.message || 'Failed to delete post');
    }
  };
  
  const handleRemoveTag = (tagToRemove) => {
    const updatedTags = tags.filter(tag => tag !== tagToRemove);
    setTags(updatedTags);
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
            <li><a href="/notifications">🔔 Notifications</a></li>
            <li><a href="/write">✍️ Write</a></li>
          </ul>
          <h4>Settings</h4>
          <ul>
            <li><a href="/edit-profile">👤 Edit Profile</a></li>
            <li><a href="/change-password">🔒 Change Password</a></li>
            <li><a href="/account-deletion">🔒 Delete Account</a></li>
          </ul>
        </nav>
      </aside>

      <main className="account-content">
        <h2>Welcome to your Account Portal</h2>
        <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Verified:</strong> {user.verifiedemail ? 'Yes' : 'No'}</p>

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
               {/* Delete button */}
               <button onClick={() => deleteBlog(blog.blogID)}
                className="delete-button"
                >
                Delete
               </button>
               {/* Edit button */}
               <button onClick={() => navigate(`/edit-post/${blog.blogID}`)} className="edit-button">
                Edit
               </button>


              <hr />
            </div>
          ))
        )}

        <hr />
        <h3>Create New Blog</h3>
        <div className="blog-form-section">
          {imagePreview && (
            <img src={imagePreview} alt="Preview" className="preview-image" />
          )}
          <h4>{title || 'Your Blog Title'}</h4>
          <p>{shortDesc || 'Your short description will appear here.'}</p>

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

          <textarea
            type="text"
            placeholder="Content of your post"
            value={content}
            onChange={(e) => setContent(e.target.value)}
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
          <div className="tag-list">
        {tags.map((tag, i) => (
            <span key={i} className="tag-chip">
            {tag}
            <button onClick={() => handleRemoveTag(tag)}>X</button>  {/* Add a button to remove tag */}
            </span>
        ))}
        </div>
          

          <input type="file" accept="image/*" onChange={handleImageChange} />

          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <button onClick={handlePublish} className="publish-button">Publish</button>
            <button onClick={handleSaveDraft} className="draft-button">Save as Draft</button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AccountPortal;

