import Vue from 'vue';
import axios from 'axios';

// EP to verify a token from google
export default function(token) {
  return axios.post('https://www.googleapis.com/oauth2/v3/tokeninfo', {
    id_token: token
  });
}
