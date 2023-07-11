import requests
import json

all_events_url = 'https://api.sandbox.viator.com/partner/products/search'
product_header = {
    "exp-api-key": API_KEY,
    "Accept-Language": "en",
    "Accept": "application/json;version=2.0"
    }
availability_header = {
    "Accept": "application/json;version=2.0",
    "exp-api-key": API_KEY
    }

payload = {
"filtering": {
        "destination": 651,
        #"tags": [11919],
        "lowestPrice": 5,
        "highestPrice": 500,
        "startDate": '2023-07-19',
        "endDate": '2023-07-30',
        "includeAutomaticTranslations": True,
        "confirmationType": "INSTANT",
        "durationInMi nutes": {"from": 20, "to": 540},
        "rating": {"from": 3, "to": 5}
    },
    "sorting": {"sort": "TRAVELER_RATING", "order": "DESCENDING"},
    "pagination": {"start": 1, "count": 50},
    "currency": "USD"
}

product_response = requests.post(all_events_url, headers=product_header, json=payload)
product_response.raise_for_status()  # Raise an exception if an HTTP error occurred
product_response = product_response.json()

product_codes = []
for product in product_response['products']:
    product_codes.append(product['productCode'])

print(product_codes)

confirm_response = requests.get(url=f'https://api.sandbox.viator.com/partner/availability/schedules/6471MUSEUM', headers=availability_header)
confirm_response = confirm_response.json()

with open('availability.json', 'w') as f:
    json.dump(confirm_response, f, indent=4)