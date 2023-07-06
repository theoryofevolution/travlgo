import requests

api_key = "3d28194b-f857-4334-930f-36540f9bf313"
endpoint_url = "https://api.example.com/viator/endpoint"  # Replace with the actual endpoint URL

# Set up the API request headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Api-Key": api_key
}

# Make the API call
response = requests.get(endpoint_url, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Successful API call
    data = response.json()
    # Process the data as per your requirements
    print(data)
else:
    # API call failed
    print("API request failed with status code:", response.status_code)
    print("Error message:", response.text)