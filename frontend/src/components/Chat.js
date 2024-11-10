import React, { useEffect, useState, useRef } from "react";
import MessageInput from "./MessageInput";
import axios from "../services/api";
import "./Chat.css";
import { useAuth } from "../context/AuthContext";
import { CircularProgress } from "@mui/material";

const Chat = ({ chatId, onSelectChat }) => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatId) {
      axios
        .get(`/get_chat?chatId=${chatId}`)
        .then((response) => setMessages(response.data.history))
        .catch((error) => console.error("Error fetching chat:", error));
    }
  }, [chatId]);

  const checkCall = async (chatId, text) => {
    await axios
      .post("/check", { chatId, messageInput: text })
      .then((response) => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: "user", message_text: text },
          { sender: "bot", message_text: response.data.response },
        ]);
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
      })
      .catch((error) => console.error("Error sending message:", error));
  };

  const sendMessage = async (text) => {
    try {
      setLoading(true);
      if (chatId) {
        if (text) {
          await checkCall(chatId, text);
        }
      } else if (text) {
        const res = await axios.post("/start_chat", {
          userId: user.email,
        });
        console.log(res, "*****");
        await checkCall(res.data.chatId, text);
        onSelectChat(chatId);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
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
            </div>
          ))
        )}
        <div ref={chatEndRef} />
      </div>
      {loading && <CircularProgress color="primary" size={60} thickness={5} />}

      <MessageInput onSendMessage={sendMessage} />
    </div>
  );
};

export default Chat;
