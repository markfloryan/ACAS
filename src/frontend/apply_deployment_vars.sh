#!/bin/bash

source /config/deployment_vars

# Hide DEBUG buttons
sed -i "s|debugLogin: true|debugLogin: false|" /app/src/components/LoginCard.vue

# Set IN_PROD to true
sed -i "s|IN_PROD = false|IN_PROD = true|" /app/src/constants/index.js

# Set PROD_API
sed -i "s|.*const PRODUCTION_API =.*|const PRODUCTION_API = 'https://$DOMAIN/api';|" /app/src/constants/index.js

# Set Client ID
sed -i "s|.*client_id:.*|client_id: '$CLIENT_ID',|" /app/src/vuex/modules/Auth.js