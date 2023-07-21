import requests
import json
import streamlit as st
import importlib
url = 'https://api.viator.com/partner/products/search'
destination = 'Paris, Île-de-France'
start_date = '2023-07-21'
end_date = '2023-07-28'
user_tags = ['Excellent Quality', 'Adventure Tours', 'Family-friendly'] 
event_number = 12
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
            tag_ids.append(data['tag'])
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
        "startDate": start_date,
        "endDate": end_date,
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

with open('activities.json', 'w') as f:
        json.dump(activities_data, f, indent=4)

for index, tag in enumerate(tag_ids):
    custom_payload = {
    "filtering": {
            "destination": destination_id,
            "tags": [tag],
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
        "pagination": {"start": 1, "count": event_number},
        "currency": "USD"
    }
    response_custom = requests.post(url, headers=header, json=custom_payload)
    custom_activities = response_custom.json()
    custom_data.append(custom_activities['products'])

custom_data = [[item for sublist in custom_data for item in sublist]]
with open('custom.json', 'w') as f:
        json.dump(custom_data, f, indent=4)

matched = {}
print("matching data")
for data in activities_data[0]:
    matched[data['productCode']] = data
print("matching custom")
for custom in custom_data[0]:
    if custom['productCode'] not in matched:
        matched[custom['productCode']] = custom
    elif matched[custom['productCode']] != custom:
        matched[custom['productCode']] = custom

with open('matched.json', 'w') as f:
        json.dump(matched, f, indent=4)