import json
import requests
import extractor
import openai
import datetime
import streamlit as st
API_KEY = st.secrets["API_KEY_VIATOR"]
url = 'https://api.sandbox.viator.com/partner/products/search'
global destinationId, custom_activities, complete_activities_data, tag_ids

def check_availability(product_code):
    url = f"https://api.viator.com/partner/availability/schedules/{product_code}"
    headers = {
        "exp-api-key": '3d28194b-f857-4334-930f-36540f9bf313',
        "Accept": "application/json;version=2.0"
    }
    

    response = requests.get(url, headers=headers)
    availability_data = response.json()
    return availability_data

def viator_post_request(destination:str, start_date, end_date, user_tags:list, event_number:int):
    activities_data = []
    custom_data = []
    with open('destinations.json') as file:
        destination_data = json.load(file)
    for data in destination_data['data']:
        if data['destinationName'] == destination:
            destination_id = data['destinationId']
    with open('english_tags.json') as file:
        tags_data = json.load(file)


    tag_ids = []
    for data in tags_data['tags']:
        for tags in user_tags:
            if data['tagNameEn'] == tags:
                tag_ids.append(data['tagId'])

    header = {
        "exp-api-key": API_KEY,
        "Accept-Language": "en",
        "Accept": "application/json;version=2.0"
        }
    
    payload = {
    "filtering": {
            "destination": destination_id,
            "lowestPrice": 5,
            "highestPrice": 500,
            "startDate": str(start_date),
            "endDate": str(end_date),
            "includeAutomaticTranslations": True,
            "confirmationType": "INSTANT",
            "durationInMinutes": {"from": 20, "to": 1080},
            "rating": {"from": 3, "to": 5}
        },
        "sorting": {"sort": "TRAVELER_RATING", "order": "DESCENDING"},
        "pagination": {"start": 1, "count": int(event_number/2)},
        "currency": "USD"
    }
    response = requests.post(url, headers=header, json=payload)
    activities = response.json()
    activities_data.append(activities['products'])
    with open('normal.json', 'w') as f:
        json.dump(activities_data, f, indent=4)

    custom_payload = {
    "filtering": {
            "destination": destination_id,
            "tags": tag_ids,
            "lowestPrice": 5,
            "highestPrice": 500,
            "startDate": str(start_date),
            "endDate": str(end_date),
            "includeAutomaticTranslations": True,
            "confirmationType": "INSTANT",
            "durationInMinutes": {"from": 20, "to": 540},
            "rating": {"from": 3, "to": 5}
        },
        "sorting": {"sort": "TRAVELER_RATING", "order": "DESCENDING"},
        "pagination": {"start": 1, "count": int(event_number/2)},
        "currency": "USD"
    }
    response_custom = requests.post(url, headers=header, json=custom_payload)
    custom_activities = response_custom.json()
    custom_data.append(custom_activities['products'])

    with open('custom.json', 'w') as f:
        json.dump(custom_data, f, indent=4)

    matched = {}

    for data in activities_data[0]:
        matched[data['productCode']] = data

    for custom in custom_data[0]:
        if custom['productCode'] not in matched:
            matched[custom['productCode']] = custom
        elif matched[custom['productCode']] != custom:
            matched[custom['productCode']] = custom
    
    extracted_values = extractor.extract_product_info(matched)

    return extracted_values

# Example usage:

product_code = "62330P2"
availability = check_availability(product_code)
print(availability)

def itinerary_creation(extracted_values, start_date, end_date):
    pass