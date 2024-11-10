// src/components/Layout.js
import React from "react";
import Nav from "./Nav";
import { useAuth } from "../context/AuthContext"; // Import AuthContext to check authentication

function Layout({ children }) {
  const { user } = useAuth();

  return (
    <div className="layout">
      {user && <Nav />} {/* Show Nav only if user is authenticated */}
      <main className="content">
        {children}
      </main>
    </div>
  );
}

export default Layout;
