import openai
import json

openai.api_key = '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'


# Step 2: Prepare the data
viator_data = json.load(open("activities.json"))
user_data = json.load(open("user_data.json"))


# Merge the extracted information
combined_data = {
    "viator_info": viator_data,
    "user_info": user_data
}

# Step 3: Generate the itinerary using GPT-3.5 model

prompt = f"Generate a personalized travel itinerary using the following data:\n{json.dumps(combined_data)}"
response = openai.Completion.create(
    engine="text-davinci-003",  # or any other GPT-3.5 variant
    prompt=prompt,
    max_tokens=500,  # Adjust as needed
    n=1,  # Generate a single response
    stop=None,  # Stop generating after a certain token (optional)
)

generated_itinerary = response.choices[0].text.strip()

# Step 4: Parse and present the generated itinerary
# Extract relevant information from the generated response
# Format and present the itinerary to the user
print(generated_itinerary)
