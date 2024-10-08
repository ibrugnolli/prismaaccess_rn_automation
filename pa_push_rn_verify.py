import requests
import json
import xml.etree.ElementTree as ET
import csv
from requests.auth import HTTPBasicAuth
import sys
from time import sleep,time, strftime, localtime
from datetime import datetime
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

   url = "https://api.sase.paloaltonetworks.com/sse/config/v1/config-versions/candidate:push"

   headers = {
       'Accept': 'application/json',
       'Authorization': 'Bearer ' + p_token
   }
   params = {
       "folder": "Shared"
   }

   payload = json.dumps({
     "description": "string",
     "folders": [
      #   "Mobile Users Container",
         "Remote Networks",
      #   "Service Connections"
     ]
   })

   #exit(0)
   response = requests.request("POST", url, headers=headers, data=payload)
   data = response.json()
   json_formatted_str = json.dumps(data, indent=2)
   #print(json_formatted_str)

   jobid = data["job_id"]

   url = "https://api.sase.paloaltonetworks.com/sse/config/v1/jobs"
   params = {}
   payload = {}

   start_time = datetime.now()

   #jobid = sys.argv[1]
   forw  = True
   validation = False
   while forw:
      r = requests.request("GET", url, headers=headers, params=params, data=payload)
      data = r.json()
      json_formatted_str = json.dumps(data, indent=2)
      #print(json_formatted_str)
      all_finish = True
      end_time = datetime.now()
      delta = end_time - start_time
      hours, remainder = divmod(delta.total_seconds(), 3600)
      minutes, seconds = divmod(remainder, 60)
      time_range = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
      print("\n#### Time:", time_range," ####")

      for record in data["data"]:
         if record["parent_id"] == jobid:
            print("\nCommit Job")
            print("Commit Type:"+ record["device_name"])
            print("Result:"+record["result_str"])
            print("Status:"+record["status_str"])
            print("Type:"+record["type_str"])
            print("Summary:"+record["summary"])
            if record["status_str"] != "FIN" and record["status_str"] != "PUSHFAIL":
               all_finish = False
               forw = True
            if (record["status_str"] == "FIN" or record["status_str"] == "PUSHFAIL") and all_finish:
               forw = False
         if record["id"] == jobid:
            if not (record["status_str"] == "FIN" and validation):
               print("\nValidation Job")
               print("Result:"+record["result_str"])
               print("Status:"+record["status_str"])
               if record["status_str"] == "FIN":
                  validation = True

      sleep(20)


if __name__ == '__main__':
    main()