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
import pa_update_ikegw
import pa_update_ipsec
import pa_update_rn


def get_ids(p_url,name,p_token):
   url = p_url
   headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + p_token
   }
   payload = {}
   params = {
      "folder": "Remote Networks",
   }
   response = requests.request("GET", url, headers=headers, data=payload, params=params)
   data = response.json()
   json_formatted_str = json.dumps(data, indent=2)
   #print(json_formatted_str)
   try:
      for record in data["data"]:
         if record["name"] == name:
            #print(record["id"])
            return record["id"]
   except:
      return None







def main():
   p_token=pa_create_token.verify_api_access()
   if p_token == None:
      exit(0)
   
   url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ike-gateways"
   id = get_ids(url,pa_env.ike_gw_name,p_token)
   #print(id)
   if id != None:
      pa_update_ikegw.update_ikegw(id,p_token)

   url = "https://api.sase.paloaltonetworks.com/sse/config/v1/ipsec-tunnels"
   id = get_ids(url,pa_env.ipsec_tunnel_name,p_token)
   #print(id)
   if id != None:
      pa_update_ipsec.update_ipsec(id,p_token)
   
   #exit(0)

   url = "https://api.sase.paloaltonetworks.com/sse/config/v1/remote-networks"
   id = get_ids(url,pa_env.rn_name,p_token)
   #print(id)
   if id != None:
      pa_update_rn.update_rn(id,p_token)
   print("OK")


if __name__ == '__main__':
   main()

#appcount=len(data["data"])
#print("number of apps: " + str(appcount))

