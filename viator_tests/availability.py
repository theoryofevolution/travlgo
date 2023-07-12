import requests
from datetime import datetime, timedelta
import json

# Set the API key
api_key = "3d28194b-f857-4334-930f-36540f9bf313"

# Set product code
product_code = "100972P3"

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

response = requests.get(url_2, headers=headers_2)
data = response.json()

with open('info.json', 'w') as f:
        json.dump(data, f, indent=4)

"""
# Check if the request was successful
if response.status_code == 200:
    # Extract the availability and pricing data from the response
    data = response.json()

    # Iterate over bookable items
    for bookable_item in data["bookableItems"]:
        # Iterate over seasons
        for season in bookable_item["seasons"]:
            season_start_date = datetime.strptime(season["startDate"], "%Y-%m-%d")
            
            # Check if the season falls within the specified date range
            if start_datetime <= season_start_date <= end_datetime:
                # Iterate over operating hours
                for operating_hour in season["operatingHours"]:
                    day_of_week = operating_hour["dayOfWeek"]
                    opening_time = datetime.strptime(operating_hour["operatingHours"][0]["opensAt"], "%H:%M:%S").time()
                    closing_time = datetime.strptime(operating_hour["operatingHours"][0]["closesAt"], "%H:%M:%S").time()

                    # Iterate over dates within the season
                    current_date = season_start_date
                    while current_date <= end_datetime:
                        # Check if the date is not in the unavailable dates
                        if all(unavailable_date["date"] != current_date.strftime("%Y-%m-%d") for unavailable_date in season["unavailableDates"]):
                            available_start_time = datetime.combine(current_date, opening_time)
                            available_end_time = datetime.combine(current_date, closing_time)

                            # Print the available time slot
                            print(f"Available on {day_of_week} - {current_date.strftime('%Y-%m-%d')}: {available_start_time.strftime('%H:%M:%S')} - {available_end_time.strftime('%H:%M:%S')}")

                        # Move to the next date
                        current_date += timedelta(days=1)
else:
    # Request was not successful, print the error message
    print(f"Error: {response.status_code} - {response.text}")
"""