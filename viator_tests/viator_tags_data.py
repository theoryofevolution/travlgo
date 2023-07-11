import requests
import json

url = "https://api.sandbox.viator.com/partner/products/tags"
headers = {
    "Accept": "application/json;version=2.0",
    "exp-api-key": api_key
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    tags_data = response.json()
    # Process the tags_data as needed

    # Save the response data to a JSON file
    with open("tags_data.json", "w") as file:
        json.dump(tags_data, file, indent=4)
        print("Tags data saved to tags_data.json")
else:
    print("Error:", response.status_code)