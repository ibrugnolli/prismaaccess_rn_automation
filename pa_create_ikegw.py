import requests
import json
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
import sys, os


here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, ".."))
sys.path.insert(0, project_root)

import pa_env
import pa_create_token

def main():

   p_token=pa_create_token.verify_api_access()
   if p_token == None:
      exit(0)
   p_ike_gw_name = pa_env.ike_gw_name
   p_ike_secret = pa_env.ike_secret
   p_local_id = pa_env.prisma_access_fqdn_id
   p_peer_id = pa_env.remote_branch_fqdn_id



   #print(p_token)
   url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ike-gateways"
   headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + p_token
   }
   params = {
      "folder": "Remote Networks",
   }

   payload = json.dumps({
     "authentication": {
       "pre_shared_key": {
         "key": p_ike_secret
      }
     },
     "local_id": {
       "id": p_local_id,
       "type": "ufqdn"
     },
     "name": p_ike_gw_name,
     "peer_address": {
       "dynamic": {}
     },
     "peer_id": {
       "id": p_peer_id,
       "type": "ufqdn"
     },
     "protocol": {
       "ikev1": {
         "dpd": {
           "enable": True
         },
         "ike_crypto_profile": "Others-IKE-Crypto-Default"
       },
       "ikev2": {
         "dpd": {
           "enable": True
         },
         "ike_crypto_profile": "Others-IKE-Crypto-Default"
       },
       "version": "ikev2-preferred"
     },
     "protocol_common": {
       "fragmentation": {
         "enable": False
       },
       "nat_traversal": {
         "enable": True
       },
       "passive_mode": True
     }
   })
   #print(headers)
   #print(response.status_code)
   #data = response.json()
   #json_formatted_str = json.dumps(data, indent=2)
   #print(json_formatted_str)
   try:
      response = requests.request("POST", url, headers=headers, params=params, data=payload)
      data = response.json()

      if response.status_code == 200 or response.status_code == 201:
         print("Ike Gateway Created Successfull")
         print("Ike Gateway ID: " + data["id"])
      else:
         for record in data["_errors"]:
            print("Ike Gateway Created Unsuccessful. Error Code " + str(response.status_code)+ ": " + record["details"]["message"])
   except:
      print("Error connecting to Prisma Cloud")
   #appcount=len(data["data"])
   #print("number of apps: " + str(appcount))



if __name__ == '__main__':
   main()
