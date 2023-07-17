import requests
from datetime import datetime, timedelta
import json
import time
import streamlit as st
# Set the API key
api_key = st.secrets["API_KEY_VIATOR"]

def available_times(start_datetime, data):
    time = {}
    initial = []
    for season in data['bookableItems']:
        for timeframe in season['seasons']:
            if datetime.strptime(timeframe['startDate'], "%Y-%m-%d") <= start_datetime:
                if timeframe['pricingRecords']:
                    for times in timeframe['pricingRecords']:
                        #time.append({'daysOfWeek': times['daysOfWeek']})
                        time['daysOfWeek'] = times['daysOfWeek']
                        if 'timedEntries' in times:
                            for starttime in times['timedEntries']:
                                initial.append(starttime['startTime'])
                            #time.append({'startTime': initial})
                                time['startTime'] = initial
                    return time
                elif 'operatingHours' in timeframe:
                    for hours in timeframe['operatingHours']:
                        time['daysOfWeek'] =  hours['dayOfWeek']
                        if hours['operatingHours']:
                            for opensat in hours['operatingHours']:
                                initial.append(opensat['opensAt'])
                                time['startTime'] = initial
                    return time
            else:
                continue
    return -1

def get_dates_in_between(start_date, end_date):
    # Create a list to store the dates
    dates_list = []

    # Generate dates in between start and end dates
    start_date += timedelta(days=1)
    current_date = start_date
    while current_date < end_date:
        dates_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return dates_list

def find_all_value_indices(json_data, search_value, key_path=""):
    indices = []
    if isinstance(json_data, list):
        for index, item in enumerate(json_data):
            indices.extend(find_all_value_indices(item, search_value, f'{key_path}[{index}]'))
    elif isinstance(json_data, dict):
        for key, value in json_data.items():
            if value == search_value:
                indices.append(f'{key_path}.{key}')
            indices.extend(find_all_value_indices(value, search_value, f'{key_path}.{key}'))
    return indices

def available(start_datetime, end_datetime, product_code):
    url = f"https://api.sandbox.viator.com/partner/availability/schedules/{product_code}"
    headers = {
    "Accept": "application/json;version=2.0",
    "exp-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    #start_datetime = datetime.strptime(start_datetime, "%Y-%m-%d")
    #end_datetime = datetime.strptime(end_datetime, "%Y-%m-%d")
    dates = get_dates_in_between(start_datetime, end_datetime)
    times = available_times(start_datetime, data)
    for search_value in dates:
        value_indices = find_all_value_indices(data, search_value)
        if value_indices:
            dates.remove(search_value)
    return dates, times