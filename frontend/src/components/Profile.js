import React, { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import jwt_decode from 'jwt-decode';
import { useLocation } from 'react-router-dom';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function Profile() {
  const { user, login } = useAuth();
  const query = useQuery();
  const token = query.get('token');

  useEffect(() => {
    if (token) {
      try {
        jwt_decode(token);  // Validate the token format
        login(token);       // Log in and set user in context
      } catch (err) {
        console.error("Invalid token format:", err);
      }
    }
  }, [token, login]);

  if (!user) return <p>User not authenticated</p>;

  return (
    <div>
      <h1>User Profile</h1>
      <p><strong>Name:</strong> {user.nickname || user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>
      {/* Display other fields from the decoded token if available */}
    </div>
  );
}

export default Profile;
