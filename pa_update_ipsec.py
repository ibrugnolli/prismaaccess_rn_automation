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

def update_ipsec(id,p_token):

    if p_token == None:
        exit(0)    
    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ipsec-tunnels/" + id

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + p_token
    }
    params = {}

    payload = json.dumps({
      "anti_replay": True,
      "auto_key": {
        "ike_gateway": [
          {
            "name": pa_env.ike_gw_name
          }
        ],
        "ipsec_crypto_profile": "Others-IPSec-Crypto-Default",

      },
      "copy_tos": False,
      "enable_gre_encapsulation": False,
      "name": pa_env.ipsec_tunnel_name,

    })


    #print(headers)
    #print(payload)
    #exit(0)
    #json_formatted_str = json.dumps(data, indent=2)
    #print(response.status_code)
    #print(json_formatted_str)
    #appcount=len(data["data"])
    #print("number of apps: " + str(appcount))
    try:
        response = requests.request("PUT", url, headers=headers, params=params, data=payload)
        data = response.json()
        if response.status_code == 200 or response.status_code == 201:
           print("Ipsec Tunnel Updated Successfull")
           print("Ipsec Tunnel ID: " + data["id"])
        else:
           for record in data["_errors"]:
              print("Ipsec Tunnel Updated Unsuccessful. Error Code " + str(response.status_code)+ ": " + record["details"]["message"])
    except:
        print("Error connecting to Prisma Cloud")   


