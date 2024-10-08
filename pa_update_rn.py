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

def update_rn(id,p_token):

    if p_token == None:
        exit(0)

    url = "https://api.sase.paloaltonetworks.com/sse/config/v1/remote-networks/" + id
    #print(url)
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + p_token
    }
    params = {}

    payload = json.dumps({
      "ecmp_load_balancing": "disable",
      "ecmp_tunnels": [
        {
          "do_not_export_routes": True,
          "ipsec_tunnel": pa_env.ipsec_tunnel_name,
          "local_ip_address": pa_env.ipsec_tunnel_name,
          "name": pa_env.rn_name,
          "secret": pa_env.ike_secret,
          "summarize_mobile_user_routes": True
        }
      ],
      "ipsec_tunnel": pa_env.ipsec_tunnel_name,
      "license_type": "FWAAS-AGGREGATE",
      "name": pa_env.rn_name,
      "region": pa_env.rn_region,
      "spn_name": pa_env.rn_spn_name,
      "subnets": pa_env.rn_subnets
    })
    try:
        response = requests.request("PUT", url, headers=headers, params=params, data=payload)
        data = response.json()

        if response.status_code == 200 or response.status_code == 201:
            print("Remote Network Updated Successfull")
            print("Remote Network ID: " + data["id"])
        else:
            for record in data["_errors"]:
                print("Remote Network Update Unsuccessful. Error Code " + str(response.status_code)+ ": " + record["details"]["message"])
    except:
        print("Error connecting to Prisma Cloud")

    #json_formatted_str = json.dumps(data, indent=2)
    #print(json_formatted_str)
    #appcount=len(data["data"])
    #print("number of apps: " + str(appcount))

