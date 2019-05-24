import axios from 'axios';
import { API_URL } from '@/constants';

const instance = axios.create({
  baseURL: API_URL, // TODO : ADD PRODUCTION API URL
  timeout: 5000,
});

instance.interceptors.request.use((config) => {
  // TODO: Check if the request is coming from inside the website, and prevent sending token elsewise
  const token = localStorage.getItem('token');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
}, error => Promise.reject(error));

export default instance;