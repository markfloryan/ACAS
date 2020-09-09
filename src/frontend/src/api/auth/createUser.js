import axios from 'axios';
import { API_URL } from '@/constants/';

// EP to create a user
export default function(id_token) {
	
  return axios.post(`${API_URL}/students/`, {
    id_token: id_token
  });
}
