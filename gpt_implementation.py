import openai
import streamlit as st
import json
import integrations
import datetime

openai.api_key = st.secrets["API_KEY_OPENAI"]

user_activities = integrations.viator_post_request('Paris', "2023-08-09", "2023-08-17", ["Excellent Quality"], 6)
def run_conversation(start_date, end_date, user_activities):
    #difference = start_date - end_date
    #days_spent = difference.days
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "system", "content": """Your job is to create travel itineraries based off of travel activities data. 
                    Please return all content in a dictionary inside of a list as such
                    [{'Day 1': {'Morning 1': 'Activity Description', [activity url, activity image url, activity product code]}, 
                    {'Afternoon 1'....}, {'Evening 1'.....}}] Note that if there isn't any activities to fill a certain slot, fill it in by yourself.
                     For all full day tours, only create content for the morning. Please use this data""" + str(json.dumps(user_activities)) + "and generate for these many days spent: 4"},
                    {"role": "assistant", "content": """'Day 1': {'Morning 1': 'Activity Description', [activity url, activity image url, activity product code]}, 
                    {'Afternoon 1'....}, {'Evening 1'.....}}]"""}]
                    )
    return response['choices'][0]['message']['content']

print(run_conversation(start_date="2023-08-09", end_date="2023-08-17", user_activities=user_activities))

    
