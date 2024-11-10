import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001', // Backend server URL
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;
