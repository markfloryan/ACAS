export const IN_PROD = false;

//Token for a fake user that doesn't require google authentication
export const DEBUG_TOKEN = '12345';

// TODO: Update once we have a public url
export const API_URL = !IN_PROD ? 'http://localhost:8000/api' : 'http://hotcake.cs.virginia.edu:8000/api';

export const toastTypes = ['success', 'error', 'info']; // info is default