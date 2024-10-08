import requests
import json


url = "https://api.meraki.com/api/v1/organizations/1007544/appliance/vpn/thirdPartyVPNPeers"


payload = '''{

		"peers": [
			{
				"name": "paloalto",
				"privateSubnets": [
					"192.168.255.0/24",
                                        "10.10.1.0/24",
					"10.11.1.0/24",
                                        "10.12.1.0/24",
					"10.101.1.0/24",
					"10.102.1.0/24",
					"34.160.111.145/32"
				],
				"secret": "3comcare",
				"localId": "ibrugnolli@paloaltonetworks.com",
				"remoteId": "ibrugnolli@paloaltonetworks.com",
				"ikeVersion": "2",
				"ipsecPolicies": {
					"ikeCipherAlgo": [ "aes256" ],
					"ikeAuthAlgo": [ "sha256" ],
					"ikePrfAlgo": [ "prfsha256" ],
					"ikeDiffieHellmanGroup": [ "group2" ],
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
					"childPfsGroup": [ "disabled" ],
					"childLifetime": 3600
				},
				"networkTags": [ "all" ],
				"publicIp": "130.41.150.196"
			}
		]
}'''

headers = {
	"Content-Type": "application/json",
	"Accept": "application/json",
	"X-Cisco-Meraki-API-Key": "00c819dbd482755c0034e66e23363c9f116f88c4"
}

response = requests.request('PUT', url, headers=headers, data = payload)

print(response.status_code)
data = response.json()
json_formatted_str = json.dumps(data, indent=2)
print(json_formatted_str)

