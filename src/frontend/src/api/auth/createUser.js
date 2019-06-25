import axios from 'axios';
import { API_URL } from '@/constants/';

// EP to create a user
export default function(token) {
	
  return axios.post(`${API_URL}/students/`, {
    token: token
  });
}
