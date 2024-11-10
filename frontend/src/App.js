// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Profile from './components/Profile';
import ChatPage from './components/ChatPage';
import './App.css'

function App() {
  return (
    <AuthProvider>
        <Router>
      <div className="App">
        <Routes>
          <Route path="/profile" element={<Profile />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </div>
    </Router>
    </AuthProvider>
    
  );
}

export default App;
