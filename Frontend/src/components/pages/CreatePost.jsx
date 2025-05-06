import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './CreatePost.css'; 

/*
    Title: CreatePost Component
    Purpose:
    The purpose of this component is to provide a user interface for creating a new blog post.
    It includes a form where the user can enter the title, content, short description,
    tags, and upload an image for the blog post.
    The component also provides functionality to save the post as a draft or publish it.
*/

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

  // Fetch user data on mount
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setImagePreview(URL.createObjectURL(file));
  };

  // Function to handle the addition of tags
  const handleAddTag = (e) => {
    if (e.key === 'Enter' && tagInput.trim() && tags.length < 10) {
      setTags([...tags, tagInput.trim()]);
      setTagInput('');
    }
  };

  // Function to handle the removal of tags
  const resetForm = () => {
    setTitle('');
    setContent('');
    setShortDesc('');
    setTags([]);
    setTagInput('');
    setImage(null);
    setImagePreview(null);
  };

  // Function to handle form submission
  const handleSubmit = async (status) => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('content', content);
    formData.append('shortDescription', shortDesc);
    formData.append('tags', JSON.stringify(tags));
    formData.append('image', image);
    formData.append('status', status)

    // Check if all required fields are filled
    try {
      const response = await fetch('/api/blog/createposts', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });

    // Check if the response is ok and handle the response accordingly
      if (!response.ok) throw new Error('Blog creation failed');
      alert('Blog created successfully!');
      navigate('/account-portal')
      resetForm();
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  // Function to handle saving the post as a draft
  const handleSaveDraft = () => {
    handleSubmit('draft'); // Call handleSubmit with 'draft'
  };
  
  // Function to handle publishing the post
  const handlePublish = () => {
    handleSubmit('published'); // Call handleSubmit with 'publish'
  };
  
  // Function to handle the removal of tags
  const handleRemoveTag = (tagToRemove) => {
    const updatedTags = tags.filter(tag => tag !== tagToRemove);
    setTags(updatedTags);
  };
  
  return (
    <main>
      {/* Display loading message while fetching data */}
      <h3 className="blog-header">Create New Blog</h3>
      <div className="blog-form-section">
        {imagePreview && (
          <img src={imagePreview} alt="Preview" className="preview-image" />
        )}
        {/* Display the title and short description */}
        <h4>{title || 'Your Blog Title'}</h4>
        <p>{shortDesc || 'Your short description will appear here.'}</p>
  
        {/* Input fields for title, short description, and etc. */}
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
  
        {/* Display the tags added by the user */}
        <div className="tag-list">
          {tags.map((tag, i) => (
            <span key={i} className="tag-chip">
              {tag}
              <button onClick={() => handleRemoveTag(tag)}>X</button>
            </span>
          ))}
        </div>
          {/* Display the image if it exists */}
        <input type="file" accept="image/*" onChange={handleImageChange} />
          
          {/* Buttons for publishing and saving as draft */}
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <button onClick={handlePublish} className="publish-button">Publish</button>
          <button onClick={handleSaveDraft} className="draft-button">Save as Draft</button>
        </div>
      </div>
    </main>
  );
 
};
