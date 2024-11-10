// src/components/ChatPage.js
import React, { useState } from 'react';
import ChatList from './ChatList';
import ChatContainer from './ChatContainer'; // Using ChatContainer here
import './ChatPage.css'; // Create a main CSS file for ChatPage layout
import Header from './Header';
import Chat from './Chat';

function ChatPage() {
  const [selectedChatId, setSelectedChatId] = useState(null);

  return (
    <div className="chat-page-container">
      {/* <ChatList onSelectChat={(chatId) => setSelectedChatId(chatId)} /> */}
      <div className="main-content">
        {/* <ChatContainer chatId={selectedChatId} /> */}
        {/* <Header /> */}
        <Chat chatId={selectedChatId} onSelectChat={(chatId) => setSelectedChatId(chatId)} />
      </div>
    </div>
  );
}

export default ChatPage;
