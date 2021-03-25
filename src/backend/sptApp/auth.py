from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
import requests
import json
import os
from .models import Student

try:
    API_DEBUG = (os.environ['DEBUG'] != 'False')
except:
    API_DEBUG = False
PROF_DEBUG_TOKEN = '12345'
STUD_DEBUG_TOKEN = '54321'

# Try to get CLIENT_ID from the CLIENT_ID environment variable, otherwise use the specified default
try:
    CLIENT_ID = os.environ['CLIENT_ID']
except:
    CLIENT_ID = '250281465409-dohlj94rioi60eiqqc2mdmsh4klgcpck.apps.googleusercontent.com'

def get_bearer_token(auth_str):
    if auth_str is None:
        return None
    bearer = "Bearer "
    bearer_index = auth_str.index(bearer)
    if(bearer_index) == -1:
        return None
    bearer_token = auth_str[bearer_index+len(bearer):]
    return bearer_token

class GoogleOAuth(authentication.BaseAuthentication):

    # If not authenticated, the request will return the WWW-Authenticate string
    def authenticate_header(self, request):
        return 'Bearer realm="api"'

    def authenticate(self, request):
        token = request.query_params.get('id_token', None)
        if token is None:
            auth_str = request.META.get('HTTP_AUTHORIZATION')
            token = get_bearer_token(auth_str)

        if API_DEBUG and token == PROF_DEBUG_TOKEN:
            try:
                user = Student.objects.get(email="mrf8t@virginia.edu")
                return (user, None)
            except Student.DoesNotExist:
                return (None, None)

        elif API_DEBUG and token == STUD_DEBUG_TOKEN:
            try:
                user = Student.objects.get(email="jsnow@virginia.edu")
                return (user, None)
            except Student.DoesNotExist:
                return (None, None)

        if token is None:
            return None

        # Before calling out to google, check if the token is already in the db
        try:
            user = Student.objects.get(id_token=token)
            return (user, None)
        except:
            pass # If the user with the given id token doesn't exist, continue and call out to google

        # Call out to google here
        URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
        PARAMS = {'id_token': token}
        r = requests.post(url=URL, params=PARAMS)
        fullProfile = r.json()

        # If the request from google was bad (No user unique ID), return None
        if(not fullProfile.get('sub')):
            return None

        #Do not authorize tokens that weren't issued by google
        if(not fullProfile.get('iss') == 'accounts.google.com'):
            return None

        #Do not authorize tokens that weren't intended for this server
        if(not fullProfile.get('aud') == CLIENT_ID):
            return None

        try:
            user = Student.objects.get(email=fullProfile.get('email'))
            user.id_token = token
            user.save() # Update ID token
        except Student.DoesNotExist:
            return (None, None)

        return (user, None)
