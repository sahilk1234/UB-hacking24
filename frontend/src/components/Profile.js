// src/components/Profile.js
import React, { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLocation, useNavigate } from 'react-router-dom';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function Profile() {
  const { user, login, loading } = useAuth();
  const navigate = useNavigate();
  const query = useQuery();
  const token = query.get('token');

  useEffect(() => {
    if (token) {
      login(token); // Only log in if there is a token in the URL query
    }
  }, [token, login]);

  // Redirect to login if user is not authenticated and loading is complete
  useEffect(() => {
    if (!loading && !user) {
      navigate('/login');
    }
  }, [user, loading, navigate]);

  // Show a loading indicator while AuthContext is loading
  if (loading) return <p>Loading...</p>;

  if (!user) return null; // Prevent rendering if user data is not available

  // Access roles from the custom claim in the token
  const roles = user["https://sumit-gupta.com/roles"] || [];
  const name = user.name || "User";
  const email = user.email || "Not provided";

  return (
    <div className="card">
      <h2>Welcome to the Profile Page</h2>
      <p><strong>Name:</strong> {name}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Role:</strong> {roles.join(', ')}</p> {/* Display roles as comma-separated list */}
    </div>
  );
}

export default Profile;
