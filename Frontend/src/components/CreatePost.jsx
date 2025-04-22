import React, { useState } from 'react';

export default function CreatePost() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (status) => {
    try {
      const response = await fetch('http://localhost:5000/blog/createposts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // for sessions
        body: JSON.stringify({ title, content, status }),
      });

      const data = await response.json();
      setMessage(data.message || 'Error');
      if (response.ok) {
        setTitle('');
        setContent('');
        setMessage('Post created successfully!');
      }
    } catch (err) {
      console.error(err);
      setMessage('Server error');
    }
  };

  return (
    <div>
      <h2>Create a New Post</h2>
      <form onSubmit={(e) => e.preventDefault()}>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title" required />
        <textarea value={content} onChange={(e) => setContent(e.target.value)} placeholder="Content" required />
        <button type="button"onClick={() => handleSubmit('published')}>Publish</button>
        <button type="button" onClick={() => handleSubmit('draft')}>Save as Draft</button>
      </form>
      <p>{message}</p>
    </div>
  );
}
