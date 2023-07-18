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
    url = f"https://api.sandbox.viator.com/partner/availability/schedules/{product_code}"
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

    # Go through all bookable items
    for bookable_item in data['bookableItems']:
        for season in bookable_item['seasons']:
            start_date = datetime.strptime(season['startDate'], "%Y-%m-%d")
            end_date = datetime.strptime(season.get('endDate', '2100-12-31'), "%Y-%m-%d")  # use a far future date if 'endDate' is not present
            if start_date <= target_date_obj <= end_date:
                for records in season['pricingRecords']:
                    if target_day_of_week in records['daysOfWeek']:
                        for unavailable_dates in records['timedEntries']:
                            for dates in unavailable_dates['unavailableDates']:
                                unavailable_days.append(dates['date'])
                            if target_date not in unavailable_days:
                                available_times.append({target_date:[unavailable_dates['startTime']]})
                                available_times = unique(available_times)
    print(available_times)
    return available_times

date = "2023-08-31"
available_times = extract_available_times('44598P8', date)

from typing import Dict, List, Union, Optional, Tuple

def create_sample_data():
    events = [
        {
            'productCode': 'P01',
            'name': 'Event 1',
            'description': 'This is event 1',
            'GPT_RANK': 2,
            'available date time': {'2023-08-13': ['10:00', '13:00'], '2023-08-14': ['13:00', '16:00']},
            'event duration': 2  # Event duration in hours
        },
        {
            'productCode': 'P02',
            'name': 'Event 2',
            'description': 'This is event 2',
            'GPT_RANK': 3,
            'available date time': {'2023-08-15': ['14:00', '17:00'], '2023-08-16': ['10:00', '13:00']},
            'event duration': 2  # Event duration in hours
        },
        {
            'productCode': 'P03',
            'name': 'Event 3',
            'description': 'This is event 3',
            'GPT_RANK': 1,
            'available date time': {'2023-08-17': ['12:00', '15:00'], '2023-08-18': ['15:00', '18:00']},
            'event duration': 2  # Event duration in hours
        },
        {
            'productCode': 'P04',
            'name': 'Event 4',
            'description': 'This is event 4',
            'GPT_RANK': 4,
            'available date time': {'2023-08-19': ['16:00', '19:00'], '2023-08-20': ['11:00', '14:00']},
            'event duration': 2  # Event duration in hours
        }
    ]

    # Create an empty calendar
    calendar = [[None for _ in range(8)] for _ in range(14)]  # 14 hours from 8AM to 9PM, for 8 days

    return events, calendar

events, calendar = create_sample_data()

def plan_events(events: List[Dict[str, Union[str, int, Dict[str, List[str]]]]], calendar: List[List[Optional[str]]]) -> None:
    events = sorted(events, key=lambda x: (-x['GPT_RANK'], min(min(x['available date time'].values()))))  # Sort events based on highest rank and earliest availability

    for date_idx, date in enumerate(calendar[0]):
        for event_index, event in enumerate(events):
            if date in event['available date time']:
                for start_time in event['available date time'][date]:
                    start_hour, start_minute = map(int, start_time.split(':'))
                    end_hour = start_hour + event['event duration']

                    # Check if the time slot is available
                    if all(x is None for x in calendar[8 + start_hour - 2: 9 + end_hour + 2]):
                        # Block off event time and travel time
                        for i in range(start_hour - 2, end_hour + 2):
                            calendar[i][date_idx] = event['name'] if start_hour <= i < end_hour else 'Travel'

                        print(f"Date: {date}")
                        print(f"Event Start Time: {start_time}")
                        print(f"Event End Time: {end_hour}:{start_minute}")
                        print(f"Travel Time: 2 hours before and after the event")
                        print(f"Event Name and Code: {event['name']} ({event['productCode']})")
                        print('\n')

                        del events[event_index]  # Remove the event from the list

                        break  # Break the inner loop once an event is scheduled for a date