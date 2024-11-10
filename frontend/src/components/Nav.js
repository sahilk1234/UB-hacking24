// src/components/Nav.js
import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; // Import useAuth to access logout function
import "./Nav.css";

function Nav() {
  const { logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-logo">Healthcare Chatbot</div>
      <ul className="navbar-links">
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/chat">Chat</Link></li>
        <li><button onClick={logout} className="logout-button">Logout</button></li> {/* Use a button for logout */}
      </ul>
    </nav>
  );
}

export default Nav;
