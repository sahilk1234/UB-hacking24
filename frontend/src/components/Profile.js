import React, { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import jwt_decode from 'jwt-decode';
import { useLocation } from 'react-router-dom';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function Profile() {
  console.log('Hello')
  const { user, login } = useAuth();
  const query = useQuery();
  const token = query.get('token');
  console.log(user)
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
    <div className="card">
      <h2>Welcome to the Profile Page</h2>
      <p>This is where user information will be displayed.</p>
    </div>
  );
}

export default Profile;
