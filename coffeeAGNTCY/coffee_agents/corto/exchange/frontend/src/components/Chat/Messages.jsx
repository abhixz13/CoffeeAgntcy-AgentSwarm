import React, { useEffect, useRef } from 'react';
import Message from './Message';

export const LOCAL_STORAGE_KEY = "chat_messages";

function Messages({ messages }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Scroll to the bottom whenever messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
      <div className='chat_messages_container'>
        {messages.map((msg) => (
            <Message
                key={msg.id}
                content={msg.content}
                aiMessage={msg.role === 'assistant'}
                animate={msg.animate}
            />
        ))}
        {/* Invisible div to ensure scrolling to the bottom */}
        <div ref={messagesEndRef} />
      </div>
  );
}

export default Messages;