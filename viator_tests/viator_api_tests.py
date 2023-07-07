import json
import requests

# API endpoint and credentials
url = "https://api.sandbox.viator.com/partner/products/search"
api_key = '3d28194b-f857-4334-930f-36540f9bf313'

# Request headers
headers = {
    "exp-api-key": api_key,
    "Accept-Language": "en",
    "Accept": "application/json;version=2.0",
}

# Request payload
payload = {
    "filtering": {
        "destination": "732",
        "tags": [21972],
        "lowestPrice": 5,
        "highestPrice": 500,
        "startDate": "2023-09-03",
        "endDate": "2023-10-02",
        "includeAutomaticTranslations": True,
        "confirmationType": "INSTANT",
    },
    "sorting": {"sort": "TRAVELER_RATING", "order": "DESCENDING"},
    "pagination": {"start": 1, "count": 10},
    "currency": "USD"
}

# Send POST request
response = requests.post(url, headers=headers, json=payload)
activities = response.json()

extracted_data = {"products":[]}
i=0
for activity in activities['products']:
    product_dict = {
        f"product_{i}": {
        "product_code": activities['products'][i]['productCode'],
        "title": activities['products'][i]['title'],
        "description": activities['products'][i]['description']
        }
    }
    extracted_data["products"].append(product_dict)
    i+=1

# Specify the file path to save the JSON data
file_path = "activities.json"

# Write the activities to the JSON file
with open(file_path, "w") as json_file:
    json.dump(activities, json_file, indent=4)

file_path_extracted = "extracted_data.json"

with open(file_path_extracted, "w") as json_file:
    json.dump(extracted_data, json_file, indent=4)


print("JSON data has been saved to", file_path)
print(f"Extracted {i} products to file. JSON data has been save to", file_path_extracted)