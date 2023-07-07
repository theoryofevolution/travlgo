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
        "flags": ["LIKELY_TO_SELL_OUT", "FREE_CANCELLATION"],
        "lowestPrice": 5,
        "highestPrice": 500,
        "startDate": "2023-09-03",
        "endDate": "2023-10-02",
        "includeAutomaticTranslations": True,
        "confirmationType": "INSTANT",
        "durationInMinutes": {"from": 20, "to": 360},
        "rating": {"from": 3, "to": 5}
    },
    "sorting": {"sort": "TRAVELER_RATING", "order": "DESCENDING"},
    "pagination": {"start": 1, "count": 5},
    "currency": "USD"
}

# Send POST request
response = requests.post(url, headers=headers, json=payload)
activities = response.json()

with open('travels.json', 'w') as f:
    json.dump(activities, f)

# Access the products
products = activities['products']
product_1 = products[1]

product_1_code = product_1['productCode']
title_1 = product_1['title']
description_1 = product_1['description']
images_1 = product_1['images'][0]['variants'][7]['url']
product_url_1 = product_1['productUrl']

# Print or process the product information
print(f"Product Code: {product_1_code}")
print(f"Title: {title_1}")
print(f"Description: {description_1}")
print(f"Url: {product_url_1}")
print(f"Image: {images_1}")