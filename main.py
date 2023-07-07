import streamlit as st
import time
import json
import requests

url = "https://api.sandbox.viator.com/partner/products/search"
api_key = '3d28194b-f857-4334-930f-36540f9bf313'

# Request headers
headers = {
    "exp-api-key": api_key,
    "Accept-Language": "en",
    "Accept": "application/json;version=2.0",
}

# Request payload
payload = {
    "filtering": {
        "destination": "732",
        "tags": [21972],
        "flags": ["LIKELY_TO_SELL_OUT", "FREE_CANCELLATION"],
        "lowestPrice": 5,
        "highestPrice": 500,
        "startDate": "2023-09-03",
        "endDate": "2023-10-02",
        "includeAutomaticTranslations": True,
        "confirmationType": "INSTANT",
        "durationInMinutes": {"from": 20, "to": 360},
        "rating": {"from": 3, "to": 5}
    },
    "sorting": {"sort": "TRAVELER_RATING", "order": "DESCENDING"},
    "pagination": {"start": 1, "count": 5},
    "currency": "USD"
}

st.title('Welcome to travlgo!')
global submitted
with st.form("my_form"):
    destination = st.text_input('Final Destination:', 'Paris')
    budget = st.number_input('Budget:', min_value=0, step=10)
    arrival_date = st.date_input("Arrival Date:")
    departure_date = st.date_input("Departure Date:")
    travel_pace = st.select_slider(
    'Select your travel pace',
    options=[1, 2, 3, 4, 5], help='1 means you would like a very relaxed and comfortable trip. 5 means that you\'re really adventurous!')
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
if submitted:
    with st.spinner('Wait for it...'):
        response = requests.post(url, headers=headers, json=payload)
        activities = response.json()    
        # Access the products
        products = activities['products']
        product_1 = products[1]
        product_1_code = product_1['productCode']
        title_1 = product_1['title']
        description_1 = product_1['description']
        images_1 = product_1['images'][0]['variants'][7]['url']
        product_url_1 = product_1['productUrl']
        # Print or process the product information
        print(f"Product Code: {product_1_code}")
        print(f"Title: {title_1}")
        print(f"Description: {description_1}")
        print(f"Url: {product_url_1}")
        print(f"Image: {images_1}")
        st.success('Done!')
        st.image(images_1)
        st.text(description_1)
        st.write(f'''
            <a target="_self" href="{product_url_1}">
                <button>
                Book this tour
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )

