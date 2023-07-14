import requests
from datetime import datetime, timedelta
import json
import time
# Set the API key
api_key = "3d28194b-f857-4334-930f-36540f9bf313"

# Set product code
product_code = "126585P2"

# Set the base URL for the API
url = f"https://api.sandbox.viator.com/partner/availability/schedules/{product_code}"
url_2 = f"https://api.sandbox.viator.com/partner/products/{product_code}"


# Set the start and end dates
start_date = "2023-08-15"
end_date = "2023-08-30"

# Convert start and end dates to datetime objects
start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

# Construct the URL

# Set the request headers
headers = {
    "Accept": "application/json;version=2.0",
    "exp-api-key": api_key
}

headers_2 = {
    "Accept": "application/json;version=2.0",
    'Accept-Language': "en-US",
    "exp-api-key": api_key
}

# Send the GET request
response = requests.get(url, headers=headers)
data = response.json()
with open('availability.json', 'w') as f:
        json.dump(data, f, indent=4)

def get_dates_in_between(start_date, end_date):
    # Create a list to store the dates
    dates_list = []

    # Generate dates in between start and end dates
    current_date = start_date
    while current_date <= end_date:
        dates_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return dates_list

def find_all_value_indices(json_data, search_value, path=''):
    indices = []

    if isinstance(json_data, list):
        for index, item in enumerate(json_data):
            indices.extend(find_all_value_indices(item, search_value, path + f'[{index}]'))
    elif isinstance(json_data, dict):
        for key, value in json_data.items():
            if value == search_value:
                indices.append(path + f'.{key}')
            indices.extend(find_all_value_indices(value, search_value, path + f'.{key}'))

    return indices

dates = get_dates_in_between(start_datetime, end_datetime)
for search_value in dates:
    value_indices = find_all_value_indices(data, search_value)
    print("\n")
    if value_indices:
        print(f"The value '{search_value}' was found at the following index/key paths:")
        for index in value_indices:
            print(index)
    else:
        print(f"The value '{search_value}' was not found in the JSON data.")
