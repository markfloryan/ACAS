const IN_PROD = false;

// TODO: Update once we have a public url
export const API_URL = !IN_PROD ? 'http://localhost:8000/api' : 'http://128.143.71.210:28174/api';

export const toastTypes = ['success', 'error', 'info']; // info is default