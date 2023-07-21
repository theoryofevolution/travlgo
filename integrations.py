import json
import requests
import extractor
import openai
from datetime import datetime, timedelta
import streamlit as st
import availability
import re
import time
import ast

API_KEY = st.secrets["API_KEY_VIATOR"]
openai.api_key = st.secrets["API_KEY_OPENAI"]
url = 'https://api.viator.com/partner/products/search'
global destinationId, custom_activities, complete_activities_data, tag_ids

def parse_list(string):
  """Parses a string into a Python list.

  Args:
    string: The string to parse.

  Returns:
    A Python list.
  """

  list_items = []
  for item in string.splitlines():
    list_items.append(item)
  return list_items

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

def create_calendar(date_range):
    print("Date Range", date_range)
    calendar = [[] for _ in range((len(date_range)))]
    return calendar, date_range


def plan_events(data, date_range, calendar):
    data = sorted(data, key=lambda x: x["GPT_RATING"] if "GPT_RATING" in x else 0, reverse=True)  # Sort events based on highest rank and earliest availability
    for index_1, date in enumerate(date_range):
        print(type(date))
        events_for_the_day = []
        for event in data:
            for availability in event["availableOnDate"]:
                if str(date) in availability:
                    time_objs = [datetime.strptime(time_str, "%H:%M") for time_str in availability[date]]
                    startTime = min(time_objs)
                    event['startTime'] = str(startTime.strftime("%H:%M"))
                    event['dateSelected'] = date
                    event['endTime'] = (startTime + timedelta(minutes=event['duration'])).strftime('%H:%M')
                    events_for_the_day.append(event)
        events_for_the_day = sorted(events_for_the_day, key=lambda x: x["GPT_RATING"] if "GPT_RATING" in x else 0, reverse=True)
        if events_for_the_day == []:
            calendar[index_1].append('No found event for the day')
        else:
            calendar[index_1].append(events_for_the_day[0])
            print("events", events_for_the_day)
            del data[data.index(events_for_the_day[0])]
            del events_for_the_day[events_for_the_day.index(events_for_the_day[0])]
            second_event_possibilities = []
            for events in events_for_the_day:
                for time in events['availableOnDate']:
                    if date in time:
                        for times in time[date]:
                            time_1 = datetime.strptime(calendar[index_1][0]['endTime'], "%H:%M") + timedelta(minutes=60)
                            time_2 = datetime.strptime(times, "%H:%M")
                            if time_1 < time_2:
                                events['startTime'] = times
                                events['endTime'] = (time_2 + timedelta(minutes=events['duration'])).strftime('%H:%M')
                                second_event_possibilities.append(events)
                            else:
                                continue
            try:
                second_event_possibilities = sorted(second_event_possibilities, key=lambda x: x["GPT_RATING"] if "GPT_RATING" in x else 0, reverse=True)
                print("Second Event for the Day", second_event_possibilities)
                calendar[index_1].append(second_event_possibilities[0])
                del data[data.index(second_event_possibilities[0])]
            except:
                pass
    print("Calendar",calendar)
    print("done")
    return calendar

def itinerary_creation(destination:str, start_date, end_date, user_tags:list, event_number:int):
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
        "pagination": {"start": 1, "count": event_number},
        "currency": "USD"
    }
    response = requests.post(url, headers=header, json=payload)
    activities = response.json()
    with open("activities.json", "w") as file:
        json.dump(activities, file, indent=4)
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
    date_range = []

    #start_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
    #end_date = datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date + timedelta(days=1)

    day_itinerary={}
    while current_date < end_date:
        date_range.append(datetime.strftime(current_date, "%Y-%m-%d"))
        current_date += timedelta(days=1)
    print("test")
    try:
        for event in extracted_values:
            content = f"""Given the event description: {event['description']} rate it from 0.00 to 5.00 based on how good it is for a family. Only return the single number as a float. Do not apologize, or contain any words in your reponse."""
            example = "4.9"
            rating = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = [{"role": "system", "content": content}, {"role": "assistant", "content": example}])
            print(rating)
            try:
                event['GPT_RATING'] = float(re.findall(r'\d+(?:\.\d+)?', rating['choices'][0]['message']['content'])[0])
            except:
                pass
            time.sleep(1)
            print("test")
    except:
        pass
    print("creating calendar")
    calendar, date_range = create_calendar(date_range)
    calendar = plan_events(extracted_values, date_range, calendar)
    print(calendar)
    return calendar