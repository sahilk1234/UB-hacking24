import React from 'react';
import Chat from './Chat';
import './ChatContainer.css';

const ChatContainer = ({ chatId }) => {
  return (
    <div className="chat-center-container">
      <Chat chatId={chatId} />
    </div>
  );
};

export default ChatContainer;
