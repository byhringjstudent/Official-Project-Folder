import React from 'react';

export default function KnowledgeBase() {
  const openBaseChat = () => {
    window.open(
      'https://sunbird-full-fully.ngrok-free.app',
      'BaseChatWindow',
      'width=1000,height=900'
    );
  };

  return (
    <div style={{ padding: '2rem' }}>
      {/* Chat Bubble Greeting */}
      <div
        style={{
          maxWidth: '900px',
          margin: '0 auto 2rem auto',
          padding: '1.5rem 2rem',
          backgroundColor: '#808080',
          color: 'white',
          borderRadius: '20px',
          position: 'relative',
          fontSize: '1.25rem',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
          lineHeight: '1.6',
        }}
      >
        <p style={{ margin: 0 }}>
          Hi! My name is <strong>Base Chat</strong>. I'm your personal Estate Planning AI Assistant.
          Ask any questions about wills, trusts, or anything else — and don’t forget to log in to get started with your documents!
        </p>

        {/* Triangle Tail */}
        <div
          style={{
            position: 'absolute',
            bottom: '-20px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 0,
            height: 0,
            borderLeft: '20px solid transparent',
            borderRight: '20px solid transparent',
            borderTop: '20px solid #808080',
          }}
        ></div>
      </div>

      {/* Chatbot iFrame Section */}
      <div
        style={{
          padding: '1.5rem',
          background: '#f1C40f',
          border: '1px solid #ccc',
          borderRadius: '12px',
          maxWidth: '2000px',
          marginInline: 'auto',
          boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
        }}
      >
        <iframe
          src="https://sunbird-full-fully.ngrok-free.app"
          sandbox="allow-scripts allow-same-origin allow-forms"
          title="Ragie Chatbot"
          style={{
            width: '100%',
            height: '900px',
            border: 'none',
            borderRadius: '12px',
            overflow: 'hidden',
          }}
        ></iframe>
             {/* Section 8: Footer */}
             <footer className="footer">
             <p>© 2025 LegacyIQ · Privacy · For Support, Contact us at {""}
               <a href="mailto:legacyiqdevteam@outlook.com" className="text-blue-500 hover:underline">
               legacyiqdevteam@outlook.com
               </a>
             </p>
           </footer>
         </div>
         </div>
       );
      }