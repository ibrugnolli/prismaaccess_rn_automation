#!/usr/bin/env python

import requests
import json
import sys, os


here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, ".."))
sys.path.insert(0, project_root)

import pa_env  # noqa

def verify_api(api_url)->bool:
	p_token= pa_env.X_PAN_KEY
	#exit(0)

	headers = {
	#    'Accept': 'application/json',
		'header-api-key':  p_token
	}
	params = {}
	#payload = json.dumps({'timespan': p_timespan , 'statuses': ["Online"]})

	payload = json.dumps({"serviceType": "gp_portal", "addrType": "all","location": "deployed"})
	#print(headers)
	try:
		r = requests.request("POST", api_url, headers=headers, data=payload)
		if r.status_code == 200:
			data = r.json()
			#json_formatted_str = json.dumps(data, indent=2)
			#print(json_formatted_str)
			print("Enviroment Found - API Key OK")
			return True
		else:
			print("Incorrect Enviroment")
			return False
	except:
		print("Unable to contact Prisma cloud")
		return False


def get_ips(api_url, stype)->bool:
	p_token= pa_env.X_PAN_KEY
	headers = {
		'header-api-key':  p_token
	}
	params = {}
	payload = json.dumps({"serviceType": stype, "addrType": "all","location": "deployed"})
	try:
		r = requests.request("POST", api_url, headers=headers, data=payload)
		if r.status_code == 200:
			data = r.json()
			#json_formatted_str = json.dumps(data, indent=2)
			#print(json_formatted_str)
                        #print("URL and API Key OK")
		elif r.status_code == 400:
			data = r.json()
			print(data["result"])
			return False
		else:
			print("There is an issue connecting to the Meraki platform.  Please check the API Key")
			return False
	except:
		print("Unable to contact Meraki cloud")
		return False
	ip_list=[]
	for record in data["result"]:
		for address in record["address_details"]:
			#print(address)
			if address["addressType"] == "active":
				for node_name in address["node_name"]:
					if node_name == pa_env.rn_name:
						#print(address["address"])
						ip_list.append(address["address"])

	if not ip_list:
		print("Public IP Address Not provisioned yet")
	else:
		#print(ip_list[0])
		text_to_insert='public_ip_address="'+ip_list[0]+'"\n'
		print(text_to_insert)
		file_name = "pa_env.py"
		with open(file_name, 'a') as file:
			file.write("\n")
			file.write(text_to_insert)

	#print(ip_list)
	#print(zone_list)
	#print(service_list)
	#print(location_list)





def main():
	env_list = ["lab","prod","prod2", "prod3", "prod4", "prod5", "prod6","lab"]
	correct_url = ""
	for env in env_list:
		print("Testing Enviroment: "+ env)
		url = "https://api." + env + ".datapath.prismaaccess.com/getPrismaAccessIP/v2"
		#print("trying URL: "+ url)
		if verify_api(url) == True:
			correct_url = url
			break
	if correct_url != "":
		#print(correct_url)
		print("\nFetching Remote Networks IP addresses")
		get_ips(correct_url,"remote_network")


	else:
		print("no valid API")


if __name__ == '__main__':
	main()

