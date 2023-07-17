import requests
import json
import streamlit as st

all_events_url = 'https://api.sandbox.viator.com/partner/products/search'
product_header = {
    "exp-api-key": "",
    "Accept-Language": "en",
    "Accept": "application/json;version=2.0"
    }


def location_event_data(destinationId:int, start_date:str, end_date:str):
    payload = {
    "filtering": {
        "destination": destinationId,
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

    with open('product_response.json', 'w') as f:
        json.dump(product_response, f, indent=4)

location_event_data('3092', "2023-09-08", "2023-09-08")

    
    