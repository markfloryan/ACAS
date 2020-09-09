// Production Settings. 
// Note: When the frontend container is built for production, apply_deployment_vars.sh will update the PRODUCTION_API and set IN_PROD to true
// Note: Do not change PROD_API or IN_PROD without making sure that apply_deployment_vars.sh doesn't break
const PRODUCTION_API = 'https://student-performance-tracker.xyz/api';
const IN_PROD = false;

// Constants
export const toastTypes = ['success', 'error', 'info']; // info is default
export const DEBUG_TOKEN = '12345';
const DEVELOP_API = 'http://spt-acas.com:8000/api';

// API URL
export const API_URL = IN_PROD ? PRODUCTION_API : DEVELOP_API;
