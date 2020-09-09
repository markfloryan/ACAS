import axios from 'axios';
import { API_URL } from '@/constants/';

// EP to create a professor
// Deprecated
export default function(token, isCreate) {
  return axios.post(`${API_URL}/professors/`, {
    token: token,
    isCreate: isCreate,
  });
}
