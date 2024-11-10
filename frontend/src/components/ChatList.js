import React, { useEffect, useState } from 'react';
import axios from '../services/api';
import './ChatList.css';

const ChatList = ({ onSelectChat }) => {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    axios.get('/list_chats', { params: { userId: "user-uuid" } })
      .then(response => setChats(response.data.chats))
      .catch(error => console.error("Error fetching chat list:", error));
  }, []);

  return (
    <div className="chat-list">
      <h3>Conversations</h3>
      {chats.map(chat => (
        <div key={chat.chat_id} className="chat-list-item" onClick={() => onSelectChat(chat.chat_id)}>
          <h4>{chat.conversation_name || "Unnamed Conversation"}</h4>
          <p>{new Date(chat.started_at).toLocaleString()}</p>
        </div>
      ))}
    </div>
  );
};

export default ChatList;
