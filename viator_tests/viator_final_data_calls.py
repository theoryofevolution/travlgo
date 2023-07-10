import requests
import json

API_KEY = '3d28194b-f857-4334-930f-36540f9bf313'
all_events_url = 'https://api.sandbox.viator.com/partner/products/search'
availability_url = 'https://api.sandbox.viator.com/partner/availability/schedules/bulk'
product_header = {
    "exp-api-key": API_KEY,
    "Accept-Language": "en",
    "Accept": "application/json;version=2.0"
    }


def location_event_data(destinationId:int, tags:list, start_date:str, end_date:str):
    payload = {
    "filtering": {
        "destination": destinationId,
        "tags": tags,
        "lowestPrice": 5,
        "highestPrice": 500,
        "startDate": start_date,
        "endDate": end_date,
        "includeAutomaticTranslations": True,
        "confirmationType": "INSTANT",
        "durationInMinutes": {"from": 20, "to": 540},
        "rating": {"from": 3, "to": 5}
    },
    "sorting": {"sort": "TRAVELER_RATING", "order": "DESCENDING"},
    "pagination": {"start": 1, "count": 50},
    "currency": "USD"
    }
    product_response = requests.post(all_events_url, headers=product_header, data=payload)
    product_response = product_response.json()

    i=0
    product_codes = []
    for product in product_response:
        product_codes.append(product[i]['productCode'])

    payload_confirm = {
        "productCodes": product_codes
    }

    
    