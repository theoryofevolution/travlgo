import streamlit as st
import json
import tag_lib
import integrations
import availability
import destinations
import webbrowser
import time
from datetime import datetime, timedelta, date
starter = date.today()
#ender = 
with open('english_tags.json') as file:
        tags_data = json.load(file)

with open('destinations.json') as file:
        destination_data = json.load(file)

st.set_page_config(
    page_title="travlgo",
    page_icon="travlgo_logo_v2.png",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.image("travlgo_logo_v3.png")

text_header = 'Please enter in the information below for an optimized experience.'
st.markdown(f'<p style="color:#FFFFFF;font-size:20px;border-radius:2%;">{text_header}</p>', unsafe_allow_html=True)

global submitted


with st.form("my_form"):

    initial_destination = st.selectbox('**Destination**', options = [""] + destinations.destination_names, format_func=lambda x: '' if x == '' else x)
    start_date = st.date_input('**Arrival Date**', min_value = starter)
    end_date = st.date_input('**Departure  Date**', value=start_date+timedelta(days=3), min_value=start_date+timedelta(days=2))

    user_tags = st.multiselect(
    '**Customize Your Trip**', options = tag_lib.snatch_tags)
    # Every form must have a submit button.
    submitted = st.form_submit_button('Submit')
global calendar
global dates
if submitted:
    if initial_destination=='':
        alert = st.warning('No destination is selected')
        time.sleep(3)
        alert.empty()
    else:
        dates = availability.get_dates_in_between(start_date, end_date)
        with st.spinner('Wait for it...'):
            calendar = integrations.itinerary_creation(destination=initial_destination, start_date=start_date, end_date=end_date, user_tags=user_tags, event_number=len(dates)*2)
            st.success('Success!')
        for index, days in enumerate(calendar):
            st.header(dates[index])
            for activity in days:
                if "No found event for the day" in activity:
                    st.write("No events were found for the day 😢...to make it up, here's a donut 🍩")
                else:
                    st.subheader(activity['title'])
                    st.image(activity['imageUrl'])
                    st.write(activity['description'])
                    st.write("Starts at ", activity['startTime'])
                    st.write("Ends at: ", activity['endTime'])
                    st.markdown("**_[To book this event, please click me!](%s)_**" % activity['productUrl'])
                    st.write("\n\n")
        st.balloons()