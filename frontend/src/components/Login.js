// src/components/Login.js
import React from 'react';
import { Container, Button, Typography, Box } from '@mui/material';
import { styled } from '@mui/system';

const StyledButton = styled(Button)(({ theme }) => ({
  minWidth: '180px',
  fontSize: '16px',
  fontWeight: 'bold',
  padding: '10px 20px',
  color: '#ffffff',
  borderRadius: '8px',
  textTransform: 'uppercase',
  transition: '0.3s ease-in-out',
  background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
  boxShadow: '0px 4px 15px rgba(33, 150, 243, 0.4)',
  '&:hover': {
    background: 'linear-gradient(45deg, #21CBF3 30%, #2196F3 90%)',
    boxShadow: '0px 6px 20px rgba(33, 150, 243, 0.6)',
    transform: 'translateY(-3px)',
  },
  '&:active': {
    transform: 'translateY(1px)',
    boxShadow: '0px 3px 10px rgba(33, 150, 243, 0.4)',
  },
}));

function Login() {
  const backendUrl = "http://localhost:5001"; // Update with your Flask backend URL

  const handleLogin = (role) => {
    // Redirect to the Flask backend with the selected role as a query parameter
    window.location.href = `${backendUrl}/login?role=${role}`;
  };

  return (
    <Container maxWidth="sm" style={{ textAlign: 'center', marginTop: '100px' }}>
      <Typography variant="h3" component="h1" color="primary" gutterBottom>
        Welcome to Healthcare Chatbot
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Please select your login type:
      </Typography>
      <Box mt={4} display="flex" justifyContent="center" gap={2}>
        <StyledButton
          variant="contained"
          onClick={() => handleLogin('patient')}
        >
          Login as Patient
        </StyledButton>
        <StyledButton
          variant="contained"
          onClick={() => handleLogin('doctor')}
          style={{
            background: 'linear-gradient(45deg, #673AB7 30%, #9C27B0 90%)',
          }}
        >
          Login as Doctor
        </StyledButton>
      </Box>
    </Container>
  );
}

export default Login;
