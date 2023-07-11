import json
import requests
# API endpoint and credentials
url = "https://api.sandbox.viator.com/partner/v1/taxonomy/destinations"
headers = {
    "Accept-Language": "en-US",
    "exp-api-key": api_key
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    # Process the data as neededd
else:
    print(f"Request failed with status code {response.status_code}")

def destination_attractions(name):
    for areas in data['data']:
        if areas['destinationName'] == name:
            destinationId = areas['destinationId']
    attractions_url = "https://api.sandbox.viator.com/partner/v1/search/attractions"

    attractions_headers = {
        "Accept-Language": "en-US",
        "exp-api-key": api_key,
        "Content-Type": "application/json"
    }

    attractions_data = {
        "destId": destinationId  # Replace with the actual destination ID
    }

    attractions_response = requests.post(attractions_url, headers=attractions_headers, data=attractions_data)
    attractions_response = attractions_response.json()
        # Process the data as needed
    print(attractions_response)

destination_attractions("San Francisco")