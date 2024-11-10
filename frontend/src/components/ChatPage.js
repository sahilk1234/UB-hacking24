import React, { useState } from 'react';
import ChatList from './ChatList';
import Chat from './Chat';
import Header from './Header';

function ChatPage() {
  const [selectedChatId, setSelectedChatId] = useState(null);

  return (
    <div className="app-container">
      <ChatList onSelectChat={(chatId) => setSelectedChatId(chatId)} />
      <div className="main-content">
        <Header />
        <Chat chatId={selectedChatId} />
      </div>
    </div>
  );
}

export default ChatPage;
