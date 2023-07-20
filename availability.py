import requests
from datetime import datetime, timedelta
import json
import time
import streamlit as st
# Set the API key
api_key = st.secrets["API_KEY_VIATOR"]

def date_to_day_of_week(date_str):
    date_format = "%Y-%m-%d"  # Format of the input date string
    date_obj = datetime.strptime(date_str, date_format)  # %A gives the full weekday name
    day_of_week = date_obj.strftime("%A")
    return day_of_week

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

def unique(data):
    unique_data = []
    for item in data:
        if item not in unique_data:
            unique_data.append(item)
    return unique_data

def extract_available_times(product_code: str, target_date: str):
    url = f"https://api.viator.com/partner/availability/schedules/{product_code}"
    headers = {
    "Accept": "application/json;version=2.0",
    "exp-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    with open("availability.json", "w") as file:
        json.dump(data, file, indent=4)
    # Convert the given date to a datetime object for comparison
    # Parse the target date and get the day of the week
    target_date_obj = datetime.strptime(target_date, "%Y-%m-%d")
    target_day_of_week = target_date_obj.strftime("%A").upper()
    available_times = []
    unavailable_days = []
    potential_times = []
    # Go through all bookable items
    for bookable_item in data['bookableItems']:
        for season in bookable_item['seasons']:
            start_date = datetime.strptime(season['startDate'], "%Y-%m-%d")
            end_date = datetime.strptime(season.get('endDate', '2100-12-31'), "%Y-%m-%d")  # use a far future date if 'endDate' is not present
            if start_date <= target_date_obj <= end_date:
                for records in season['pricingRecords']:
                    if target_day_of_week in records['daysOfWeek']:
                        if 'timedEntries' in records:
                            for unavailable_dates in records['timedEntries']:
                                if 'unavailableDates' in unavailable_dates:
                                    for dates in unavailable_dates['unavailableDates']:
                                        unavailable_days.append(dates['date'])
                                    if target_date not in unavailable_days:
                                        potential_times.append(unavailable_dates['startTime'])
                                        potential_times = list(set(potential_times))
                                        print("running")
                        else:
                            return ['Nothing Found']
    available_times.append({target_date:potential_times})
    if available_times[0][target_date] == []:
        return ['Nothing Found']
    else:
        return available_times

from typing import Dict, List, Union, Optional, Tuple

def create_calendar(start_date, end_date):
    get_dates_in_between(start_date, end_date)
    calendar = [[None for _ in range((len(get_dates_in_between)))]]
    return calendar


def plan_events(events: List[Dict[str, Union[str, int, Dict[str, List[str]]]]], calendar: List[List[Optional[str]]]) -> None:
    events = sorted(events, key=lambda x: (-x['GPT_RANK'], min(min(x['available date time'].values()))))  # Sort events based on highest rank and earliest availability