import requests

# Viator API credentials
VIATOR_API_KEY = '3d28194b-f857-4334-930f-36540f9bf313'

# Function to call Viator API and retrieve activities

url = 'https://api.sandbox.viator.com/partner/products/search'
headers = {
        'exp-api-key': '3d28194b-f857-4334-930f-36540f9bf313',
        'Accept-Language': 'en-US',
        'Accept': 'application/json;version=2.0',
        "filtering": {"destination": "732"},
        "currency": "USD"
    }


response = requests.post(url, headers=headers)
activities = response.json()

# Display the activities
print(activities)