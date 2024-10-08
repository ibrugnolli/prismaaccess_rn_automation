import requests
import json
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
import sys, os


here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, ".."))
sys.path.insert(0, project_root)

import pa_env  # noqa

def verify_api_access():
   # Define the URL and credentials
   p_url = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
   p_username = pa_env.pa_service_account_username
   p_password = pa_env.pa_service_account_password
   p_scope = pa_env.pa_tenant_service_group_id

   # Define the payload
   data = {
       "grant_type": "client_credentials",
       "scope": p_scope
   }

   # Define the headers
   headers = {
       "Content-Type": "application/x-www-form-urlencoded"
   }

   # Make the POST request
   try:
      r = requests.post(p_url, data=data, headers=headers, auth=HTTPBasicAuth(p_username, p_password))
      if r.status_code == 200:
         # Print the response
         data = r.json()
         #json_formatted_str = json.dumps(data, indent=2)
         #print(json_formatted_str)
         print("API Token Creation Sucessfull")
         return data["access_token"]
      else:
         print("API Token Creation Unsucessfull - Verify the parameters")
         return None
   except:
         print("API Token Creation Unsucessfull - Verify the parameters")
         return None


def main():
   p_token = verify_api_access()
   print(p_token)


if __name__ == '__main__':
   main()
