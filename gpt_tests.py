import openai
import json

openai.api_key = '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'


# Step 2: Prepare the data
viator_data = json.load(open("extracted_data.json"))
user_data = json.load(open("user_data.json"))


# Merge the extracted information
combined_data = {
    "viator_info": viator_data,
    "user_info": user_data
}


# Step 3: Generate the itinerary using GPT-3.5 Turbo model
prompt = f"""Generate a travel itinerary day by day using the data that you have been given. In between each activity
you are allowed to include some information about their travel location, or anything else that is interesting to do on the way to their next place. {json.dumps(combined_data)}
Format [YOU CAN ALSO RECOMMEND PLACES TO GO THAT ARE NOT ON THE LIST FOR FOOD AND DRINK. YOU ARE ALLOWED TO REMOVE AND REPLACE ACTIVITIES BASED ON THEIR TRAVEL PACE. IF THEY HAVE A COMFORTABLE TRAVEL PACE, ALLOW FOR 1-2 ACTIVITIES A DAY. IF THEY HAVE AN ADVENTUROUS TRAVEL PACE, INCLUDE THREE ACTIVITIES.
THE FOLLOWING IS JUST AN EXAMPLE. DO AS YOU SEE FIT. ENSURE NOT TO SUGGEST REDUNDANT TOURS OF SAME AREAS]:
Day 1:
    Morning Activity:
        [RECOMMENDATION]
    Afternoon Activity:
        [RECOMMENDATION]
    Evening Activity:
        [RECOMMENDATION]
Day 2:
    Morning Activity:
        [RECOMMENDATION]
    Afternoon Activity:
        []
    Evening Activity:
        [RECOMMENDATION]
END OF FORMAT
"""

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=500,
    temperature=0.7,
    n=1,
    stop=None,
)

generated_itinerary = response.choices[0].text.strip()

# Step 4: Parse and present the generated itinerary
# Extract relevant information from the generated response
# Format and present the itinerary to the user
print(generated_itinerary)