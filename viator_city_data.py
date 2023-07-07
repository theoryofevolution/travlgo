import json
import requests

# API endpoint and credentials
url = "https://api.sandbox.viator.com/partner/v1/taxonomy/destinations"
api_key = '3d28194b-f857-4334-930f-36540f9bf313'

headers = {
    "Accept-Language": "en-US",
    "exp-api-key": api_key
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")

file_path_extracted = "destinations.json"
destinations = response.json()
with open(file_path_extracted, "w") as json_file:
    json.dump(destinations, json_file, indent=4)
