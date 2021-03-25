// Production Settings. 
// Note: When the frontend container is built for production, apply_deployment_vars.sh will update the PRODUCTION_API and set IN_PROD to true
// Note: Do not change PROD_API or IN_PROD without making sure that apply_deployment_vars.sh doesn't break
// TODO: Prod/Dev work 
const IN_PROD = false;

const PRODUCTION_API = 'http://hotcake.cs.virginia.edu:8000/api';
const PROD_CID = '250281465409-dohlj94rioi60eiqqc2mdmsh4klgcpck.apps.googleusercontent.com';

const DEVELOP_API = 'http://localhost:8000/api';
const DEV_CID = '250281465409-v94enoqrc5p1gr7eic9fo54ss1oetjhe.apps.googleusercontent.com';


// Constants
export const toastTypes = ['success', 'error', 'info']; // info is default
// API URL
export const API_URL = IN_PROD ? PRODUCTION_API : DEVELOP_API;
// Google client ID
export const CLIENT_ID = IN_PROD ? PROD_CID : DEV_CID; 
