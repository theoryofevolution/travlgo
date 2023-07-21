import requests
import json
import streamlit as st
destination = 'Paris, Île-de-France'
2023-07-21 2023-07-28 ['Excellent Quality', 'Adventure Tours', 'Family-friendly'] 12
activities_data = []
custom_data = []
with open('destinations.json') as file:
    destination_data = json.load(file)
for data in destination_data['data']:
    if data['destinationType'] == 'CITY':
        if data['showUser'] == destination:
            destination_id = data['destinationId']

with open('english_tags.json') as file:
        tags_data = json.load(file)


tag_ids = []
for data in tags_data:
    for tags in user_tags:
        if data['tagNameEn'] == tags:
            tag_ids.append(data['tagId'])
header = {
    "exp-api-key": st.secrets['API_KEY_VIATOR'],
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
    "pagination": {"start": 1, "count": event_number},
    "currency": "USD"
}
response = requests.post(url, headers=header, json=payload)
activities = response.json()
activities_data.append(activities['products'])
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
    "pagination": {"start": 1, "count": event_number},
    "currency": "USD"
}
response_custom = requests.post(url, headers=header, json=custom_payload)
custom_activities = response_custom.json()
custom_data.append(custom_activities['products'])
matched = {}
for data in activities_data[0]:
    matched[data['productCode']] = data
for custom in custom_data[0]:
    if custom['productCode'] not in matched:
        matched[custom['productCode']] = custom
    elif matched[custom['productCode']] != custom:
        matched[custom['productCode']] = custom
extracted_values = extractor.extract_product_info(matched, start_date, end_date)
with open('extracted.json', 'w') as f:
    json.dump(extracted_values, f, indent=4)
print("DOWNLOADING TO JSON")