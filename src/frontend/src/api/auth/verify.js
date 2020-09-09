import Vue from 'vue';
import axios from 'axios';

// EP to verify an id_token from google
export default function(id_token) {
  return axios.post('https://www.googleapis.com/oauth2/v3/tokeninfo', {
    id_token: id_token
  });
}
