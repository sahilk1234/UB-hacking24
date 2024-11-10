// src/components/Layout.js
import React from "react";
import Nav from "./Nav";
import Header from "./Header"; // Import Header component for consistency in layout
import { useAuth } from "../context/AuthContext"; 
import "./Layout.css";

function Layout({ children }) {
  const { user } = useAuth();

  return (
    <div className="layout">
      {user && <Nav />} {/* Show Nav only if user is authenticated */}
      <Header />
      <main className="content">
        {children}
      </main>
    </div>
  );
}

export default Layout;
