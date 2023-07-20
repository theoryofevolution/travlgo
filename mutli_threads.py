import concurrent.futures
import openai
import streamlit as st
import re
import json
# Set up your OpenAI API credentials
openai.api_key = st.secrets['API_KEY_OPENAI']

# Define a function to make a single API request
def make_openai_request(requests):
    rating = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = requests)
    rating = rating['choices'][0]['message']['content']
    try:
        return float(re.findall(r'\d+(?:\.\d+)?', rating['choices'][0]['message']['content'])[0])
    except:
        pass

def openai_threader(data, requests):
    for events in data:
        content = f"""Given the event description: {events['description']} rate it from 0.00 to 5.00 based on how good it is for a family. Only return the single number as a float. Do not apologize, or contain any words in your reponse."""
        example = "4.9"
        requests.append([{"role": "system", "content": content}, {"role": "assistant", "content": example}])

    max_concurrent_requests = 10

    # Set the maximum number of concurrent requests
    max_concurrent_requests = 10

    # Create an executor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_requests)

    # Submit the requests to the executor
    futures = [executor.submit(make_openai_request, request) for request in requests]

    # Retrieve the results as they become available
    for future in concurrent.futures.as_completed(futures):
        response = future.result()
    # Process the response as needed
    return response
# Define a list of API requests
requests = []

with open('extracted.json') as json_file:
    data = json.load(json_file)

response = openai_threader(data, requests)
print(response)
