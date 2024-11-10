// src/components/Nav.js
import React from "react";
import { Link } from "react-router-dom";
import "./Nav.css";

function Nav() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">Healthcare Chatbot</div>
      <ul className="navbar-links">
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/chat">Chat</Link></li>
        <li><Link to="/login">Logout</Link></li>
      </ul>
    </nav>
  );
}

export default Nav;
