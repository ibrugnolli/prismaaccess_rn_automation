import requests
import json
import sys, os



here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, ".."))
sys.path.insert(0, project_root)

import pa_env
import pa_create_token

def main():
	try:
		if pa_env.public_ip_address:
			print("Public Prisma Access IP Address defined: " + pa_env.public_ip_address)
	except:
			print("Public Prisma Access IP Address not defined. Please run script pa_egress_ip.py ")
			exit(0)

	url = "https://api.meraki.com/api/v1/organizations/"+pa_env.meraki_org_id+"/appliance/vpn/thirdPartyVPNPeers"
	payload = {
	    "peers": [
	        {
	            "name": "paloalto",
	            "privateSubnets": pa_env.pa_subnets,  # Insert pa_subnets here
	            "secret": pa_env.ike_secret,
	            "localId": pa_env.remote_branch_fqdn_id,
	            "remoteId": pa_env.prisma_access_fqdn_id,
	            "ikeVersion": "2",
	            "ipsecPolicies": {
	                "ikeCipherAlgo": ["aes256"],
	                "ikeAuthAlgo": ["sha256"],
	                "ikePrfAlgo": ["prfsha256"],
	                "ikeDiffieHellmanGroup": ["group2"],
	                "ikeLifetime": 28800,
	                "childCipherAlgo": [
	                    "tripledes",
	                    "aes128",
	                    "aes192",
	                    "aes256"
	                ],
	                "childAuthAlgo": [
	                    "md5",
	                    "sha1",
	                    "sha256"
	                ],
	                "childPfsGroup": ["disabled"],
	                "childLifetime": 3600
	            },
	            "networkTags": ["all"],
	            "publicIp": pa_env.public_ip_address
	        }
	    ]
	}
	payload_json = json.dumps(payload, indent=4)
	headers = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"X-Cisco-Meraki-API-Key": pa_env.meraki_api_key
	}
	#print(payload_json)
	#print(headers)
	#exit(0)
	try:
		response = requests.request('PUT', url, headers=headers, data = payload_json)
		if response.status_code == 200:
			print("VPN to Prisma Access created/updated successfully")
		else:
			print("VPN to Prisma Access created/updated unsuccessfully. Please verify your parameters")
			if response.status_code == 404:
				print("Error code: " + str(response.status_code) + " Bad URI - please verify your org_id")
			elif response.status_code == 401:
				print("Error code: " + str(response.status_code) + " Unauthorized - please verify your API key")
			else:
				print("Error code: " + str(response.status_code))				
			#data = response.json()
			#json_formatted_str = json.dumps(data, indent=2)
			#print(json_formatted_str)
	except:
		print("Network issues connecting to Meraki Cloud")

if __name__ == '__main__':
	main()
