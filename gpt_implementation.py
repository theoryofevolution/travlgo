import openai
import streamlit as st
import json
import integrations
import datetime

openai.api_key = st.secrets["API_KEY_OPENAI"]

user_activities = integrations.viator_post_request('Paris', "2023-08-09", "2023-08-17", ["Excellent Quality"], 50)
def run_conversation(start_date, end_date, user_activities):
    content = f"""Your job is to create day by day travel itineraries based off of travel activities data. Return data in a JSON format. 
                In the json file, ensure that there is the activity description, url, image url, and product code. Classify all events
                to Morning, Evening, Night, or Full Day tags. Please use this data: {user_activities}.
                The start date for the vacation is on {start_date} and the end date is on {end_date}. Ensure that it is in JSON format"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages = [{"role": "system", "content": "Label the event based on the event description given these tags: ['Full Day', 'Half Day', '']"}])
    return response['choices'][0]['message']['content']

print(run_conversation(start_date="2023-08-09", end_date="2023-08-17", user_activities=user_activities))

    
