import json
import requests
import extractor
import openai
from datetime import datetime, timedelta
import streamlit as st
import availability
API_KEY = st.secrets["API_KEY_VIATOR"]
openai.api_key = st.secrets["API_KEY_OPENAI"]
url = 'https://api.sandbox.viator.com/partner/products/search'
global destinationId, custom_activities, complete_activities_data, tag_ids

def itinerary_creation(destination:str, start_date, end_date, user_tags:list, event_number:int):
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

    matched = {}

    for data in activities_data[0]:
        matched[data['productCode']] = data

    for custom in custom_data[0]:
        if custom['productCode'] not in matched:
            matched[custom['productCode']] = custom
        elif matched[custom['productCode']] != custom:
            matched[custom['productCode']] = custom
    
    extracted_values = extractor.extract_product_info(matched, start_date, end_date)
    with open("extracted.json", "w") as file:
        json.dump(extracted_values, file, indent=4)
    date_range = []

    start_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date

    day_itinerary={}

    while current_date < end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)

    content = f"""Across all the dates in the list {date_range} at {destination}, tell the user what to do each morning.
                Ensure that each morning is different. Suggest where they could eat food and what they could do to start each morning.
                 Do not tell them to visit any tourist attractions as that would be for the afternoon. RETURN AS PYTHON LIST"""
    example = f"""['Thing to do', 'Thing to do'...]"""
    morning = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [{"role": "system", "content": content}, {"role": "assistant", "content": example}])
    print(morning['choices'][0]['message']['content'])
    
    #content = f"""For each day in the list: {date_range} pick an event from this data {extracted_values}.
    #                Ensure that each event is different. RETURN PRODUCTCODES AS A LIST IN THIS FORMAT []"""
    #example = """EXAMPLE: ['44598P8', '6353P18', '40925P1', '6353P14', '129335P2', '6353LOUVRE', '40925P3', '6353P22', '398994P1', '343759P2', '7842P4']"""
    #afternoon = openai.ChatCompletion.create(
    #    model="gpt-4",
    #    messages = [{"role": "system", "content": content}, {"role": "assistant", "content": example}])
    #print(afternoon['choices'][0]['message']['content'])

    #content = f"""Across all the dates in the list {date_range} at {destination}, tell the user what to do each evening.
    #            Ensure that each evening is different. Suggest where they could eat food and what they could do to start each evening.
    #             Do not tell them to visit any tourist attractions as that would be for the afternoon. RETURN AS PYTHON LIST"""
    #
    evening = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [{"role": "system", "content": content}, {"role": "assistant", "content": example}])
    print(evening['choices'][0]['message']['content'])
    print(extracted_values[0:len(date_range)])
    return morning['choices'][0]['message']['content'], evening['choices'][0]['message']['content']

print(itinerary_creation('Paris', "2023-08-09", "2023-08-13", ["Excellent Quality"], 16))