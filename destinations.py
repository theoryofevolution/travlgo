import json
import requests
import streamlit as st
"""
url = "https://api.viator.com/partner/v1/taxonomy/destinations"
headers = {
    "Accept-Language": "en-US",
    "exp-api-key": st.secrets['API_KEY_VIATOR']
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    # Process the data as neededd
else:
    print(f"Request failed with status code {response.status_code}")

with open("destinations.json", "w") as file:
        json.dump(data, file, indent=4)
"""
with open('destinations.json') as json_file:
    data = json.load(json_file)
def find_product_by_id(id, data):
    for destination in data['data']:
        if id == destination['destinationId']:
            return destination['destinationName']

destination_names = []
# Iterate over the data
for item in data['data']:
    if item["destinationType"] == "CITY":
        product = find_product_by_id(item['parentId'], data)
        if product is not None:
            # If a product was found, add it to the data item
            item['showUser'] = item['destinationName'] + ", " + product
            destination_names.append(item['showUser'])

"""
print(destination_names)
# Convert the data back into a JSON string
with open("destinations.json", "w") as file:
        json.dump(data, file, indent=4)
"""