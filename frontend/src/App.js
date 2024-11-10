// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Profile from "./components/Profile";
import ChatPage from "./components/ChatPage";
import Login from "./components/Login";
import Layout from "./components/Layout"; // Import Layout
import "./App.css";

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<Login />} />
            {/* Use Layout only for authenticated pages */}
            <Route path="/profile" element={<Layout><Profile /></Layout>} />
            <Route path="/chat" element={<Layout><ChatPage /></Layout>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
