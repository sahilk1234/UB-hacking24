// src/context/AuthContext.js
import React, { createContext, useContext, useEffect, useState } from 'react';
import jwt_decode from 'jwt-decode';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      try {
        const decoded = jwt_decode(token);
        setUser(decoded);
      } catch (err) {
        console.error("Failed to decode token:", err);
        localStorage.removeItem('authToken');
      }
    }
    setLoading(false);
  }, []);

  const login = (token) => {
    try {
      const decoded = jwt_decode(token);
      setUser(decoded);
      localStorage.setItem('authToken', token);
    } catch (err) {
      console.error("Invalid token format:", err);
    }
  };

  const logout = () => {
    // Get the token and `sid` (session ID) from the JWT
    const token = localStorage.getItem('authToken');
    const decoded = token ? jwt_decode(token) : null;
    const sid = decoded ? decoded.sid : null;

    // Construct the logout URL with required parameters
    const domain = "sumit-gupta.us.auth0.com"; // Replace with your Auth0 domain
    const logoutUrl = `https://${domain}/oidc/logout?id_token_hint=${token}&post_logout_redirect_uri=http%3A%2F%2Flocalhost%3A3000%2F&logout_hint=${sid}`;

    // Clear the token from localStorage
    localStorage.removeItem('authToken');
    setUser(null);

    // Redirect to the constructed logout URL
    window.location.href = logoutUrl;
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
