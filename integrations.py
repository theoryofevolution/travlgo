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
def remove_json_object(json_data, product_code):
    return [item for item in json_data if item['productCode'] != product_code]

def date_to_day_of_week(date_str):
    date_format = "%Y-%m-%d"  # Format of the input date string
    date_obj = datetime.strptime(date_str, date_format)
    day_of_week = date_obj.strftime("%A")  # %A gives the full weekday name
    return day_of_week

# Function to convert time string to datetime object
def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M")

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
    date_range = []

    start_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date

    day_itinerary={}

    while current_date < end_date:
        date_range.append(datetime.strftime(current_date, "%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    for event in extracted_values:
        content = f"""Given the event data: {event} rate it from 0.00 to 5.00 based on how good it is for a family. Only return the single number as a float. Do not apologize, or contain any words in your reponse."""
        example = "4.9"
        rating = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{"role": "system", "content": content}, {"role": "assistant", "content": example}])
        print(event)
        print('RATING: ', rating['choices'][0]['message']['content'])
        event['GPT_RATING'] = rating['choices'][0]['message']['content']

    with open("extracted.json", "w") as file:
        json.dump(extracted_values, file, indent=4)
    #content = f"""Across all the dates in the list {date_range} at {destination}, tell the user what to do each morning.
    #            Ensure that each morning is different. Suggest where they could eat food and what they could do to start each morning.
    #             Do not tell them to visit any tourist attractions as that would be for the afternoon. RETURN AS PYTHON LIST"""
    #example = f"""['Thing to do', 'Thing to do'...]"""
    #morning = openai.ChatCompletion.create(
    #    model="gpt-4",
    #    messages = [{"role": "system", "content": content}, {"role": "assistant", "content": example}])
    #print(morning['choices'][0]['message']['content'])
    """
    final_events = []
    for date in date_range:
        sort_events = []
        for event in extracted_values:
            if date in event['availableOnDate']:
                sort_events.append(event)
        sort_events.sort(key=lambda x: x['GPT-RATING'], reverse=True)
        if sort_events == []:
            break
        else:
            extracted_values = remove_json_object(extracted_values, sort_events[0]['productCode'])
            final_events.append(sort_events[0])
    """
    """
    with open("final_events.json", "w") as file:
        json.dump(final_events, file, indent=4)
    """
    with open('final_events.json', 'r') as file:
        final_events = json.load(file)

    #content = f"""Across all the dates in the list {date_range} at {destination}, tell the user what to do each evening.
    #            Ensure that each evening is different. Suggest where they could eat food and what they could do to start each evening.
    #             Do not tell them to visit any tourist attractions as that would be for the afternoon. RETURN AS PYTHON LIST"""
    #
    """
    evening = openai.ChatCompletion.create(
        model="gpt-4",
        messages = [{"role": "system", "content": content}, {"role": "assistant", "content": example}])
    print(evening['choices'][0]['message']['content'])
    print(extracted_values[0:len(date_range)])
    return morning['choices'][0]['message']['content'], evening['choices'][0]['message']['content']
    """

#print(itinerary_creation('Paris', "2023-08-09", "2023-08-14", ["Excellent Quality"], 20))

def create_calendar(start_date, end_date):
    date_range = []

    start_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date

    while current_date < end_date:
        date_range.append(datetime.strftime(current_date, "%Y-%m-%d"))
        current_date += timedelta(days=1)

    calendar = [[] for _ in range((len(date_range)))]
    return calendar


def plan_events(data):
    for index, rating in enumerate(data):
        if rating['GPT_RATING'] == '':
            print(index)
            del data[index]
        else:
            rating['GPT_RATING'] = float(rating['GPT_RATING'])
    with open("extracted.json", "w") as file:
        json.dump(data, file, indent=4)
    data = sorted(data, key=lambda x: x["GPT_RATING"], reverse=True)  # Sort events based on highest rank and earliest availability
    return data

print(create_calendar("2023-08-09", "2023-08-14"))

with open('extracted.json', 'r') as file:
        available_events = json.load(file)

plan_events(available_events)