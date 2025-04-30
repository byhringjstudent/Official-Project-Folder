import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './CreatePost.css'; 

export default function CreatePost() {
  const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [shortDesc, setShortDesc] = useState('');
    const [tagInput, setTagInput] = useState('');
    const [status, setStatus] = useState('draft');
    const [tags, setTags] = useState([]);
    const [image, setImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

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
  
  const handleRemoveTag = (tagToRemove) => {
    const updatedTags = tags.filter(tag => tag !== tagToRemove);
    setTags(updatedTags);
  };
  
  return (
    <main>
      <h3 className="blog-header">Create New Blog</h3>
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
            <span key={i} className="tag-chip">
              {tag}
              <button onClick={() => handleRemoveTag(tag)}>X</button>
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
  );
 
};
