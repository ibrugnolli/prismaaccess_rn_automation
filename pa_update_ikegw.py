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

def update_ikegw(id,p_token):

   #p_token=pa_create_token.verify_api_access()
   if p_token == None:
      exit(0)
   #else:
   #   print(p_token)
   p_ike_gw_name = pa_env.ike_gw_name
   p_ike_secret = pa_env.ike_secret
   p_local_id = pa_env.prisma_access_fqdn_id
   p_peer_id = pa_env.remote_branch_fqdn_id



   #print(p_token)
   url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ike-gateways/" + id
   #print(url)
   #url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ike-gateways"
   headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + p_token
   }
   params = {}

    
   payload = {
    "name": pa_env.ike_gw_name,
    "peer_address": {
      "dynamic": {}
    },
    "peer_id": {
      "id": pa_env.remote_branch_fqdn_id,
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
      }
    },
    "authentication": {
      "pre_shared_key": {
        "key": pa_env.ike_secret
      }
    },
    "local_id": {
      "id": "ibrugnolli@paloaltonetworks.com",
      "type": "ufqdn"
    }
   }


   payload_json = json.dumps(payload)
   #print(payload_json)
   #print(headers)
   #print(response.status_code)
   #data = response.json()
   #json_formatted_str = json.dumps(data, indent=2)
   #print(json_formatted_str)
   try:
      response = requests.request("PUT", url, headers=headers, data=payload_json)
      data = response.json()
      json_formatted_str = json.dumps(data, indent=2)
      #print(json_formatted_str)

      if response.status_code == 200 or response.status_code == 201:
         print("Ike Gateway Updated Successfull")
         print("Ike Gateway ID: " + data["id"])
      else:
         for record in data["_errors"]:
            print("Ike Gateway Updated Unsuccessful. Error Code " + str(response.status_code)+ ": " + record["details"]["message"])
   except:
      print("Error connecting to Prisma Cloud")
   #appcount=len(data["data"])
   #print("number of apps: " + str(appcount))

