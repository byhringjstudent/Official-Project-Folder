import React from 'react';

export default function KnowledgeBase() {
  return (
    <div style={{ padding: '2rem' }}>
      {/* Bordered Top Section */}
      <div
        style={{
          backgroundColor: '#fefefe',
          border: '2px solid #F1C40F', // Gold Amber
          borderRadius: '12px',
          padding: '2rem',
          marginBottom: '2rem',
          maxWidth: '1000px',
          marginInline: 'auto',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        }}
      >
        <h2 style={{ color: '#2C3E50', marginBottom: '0.5rem' }}>
          Knowledge Base
        </h2>
        <p style={{ color: '#2C3E50', margin: 0 }}>
          Ask questions about estate planning, trusts, wills, and more.
        </p>
      </div>

      {/* Chatbot iFrame Section */}
      <div
        style={{
          padding: '1.5rem',
          background: '#f9f9f9',
          border: '1px solid #ccc',
          borderRadius: '12px',
          maxWidth: '1200px',
          marginInline: 'auto',
          boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
        }}
      >
        <iframe
          src="http://localhost:3000" // Replace with deployed URL when ready
          title="Ragie Chatbot"
          style={{
            width: '100%',
            height: '900px',
            border: 'none',
            borderRadius: '12px',
            overflow: 'hidden',
          }}
        ></iframe>
      </div>
    </div>
  );
}
