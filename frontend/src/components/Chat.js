import React, { useEffect, useState, useRef } from 'react';
import MessageInput from './MessageInput';
import axios from '../services/api';
import './Chat.css';

const Chat = ({ chatId }) => {
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatId) {
      axios.get(`/get_chat?chatId=${chatId}`)
        .then(response => setMessages(response.data.history))
        .catch(error => console.error("Error fetching chat:", error));
    }
  }, [chatId]);

  const sendMessage = (text) => {
    if (chatId && text) {
      axios.post('/check', { chatId, messageInput: text })
        .then(response => {
          setMessages(prevMessages => [
            ...prevMessages,
            { sender: 'user', message_text: text },
            { sender: 'bot', message_text: response.data.response }
          ]);
          chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => console.error("Error sending message:", error));
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-chat-message">
            <p>No messages yet. Start the conversation!</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <p>{msg.message_text}</p>
              <span className="timestamp">{new Date(msg.created_at).toLocaleTimeString()}</span>
            </div>
          ))
        )}
        <div ref={chatEndRef} />
      </div>
      <MessageInput onSendMessage={sendMessage} />
    </div>
  );
};

export default Chat;
