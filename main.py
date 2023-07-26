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
    menu_items={'Report a bug':'https://docs.google.com/forms/d/e/1FAIpQLSciIVTnEU94L3srZB5xMY3QBREzxNElsZD2rPHhIikD07IbOg/viewform'}
)

st.sidebar.image("travlgo_logo_v2.png", use_column_width=True)

text_header = "Please enter in the information below for an optimized experience."
st.markdown(f'<p style="color:#FFFFFF;font-size:20px;border-radius:2%;">{text_header}</p>', unsafe_allow_html=True)

global submitted


with st.form("my_form"):

    initial_destination = st.selectbox('**Destination**', options = [""] + destinations.destination_names, format_func=lambda x: '' if x == '' else x)
    start_date = st.date_input('**Arrival Date**', min_value = starter)
    end_date = st.date_input('**Departure  Date**', value = starter+timedelta(days=3), min_value = starter+timedelta(days=2))

    user_tags = st.multiselect(
    '**Customize Your Trip**', options = tag_lib.snatch_tags, help = "Search for your interests to help us make our results more personalized. Please choose anywhere from 1-5 options.", max_selections=5)
    # Every form must have a submit button.
    submitted = st.form_submit_button('Generate')
global calendar
global dates
if submitted:
    if initial_destination=='':
        alert = st.warning('No destination selected.')
        time.sleep(3)
        alert.empty()
    if start_date + timedelta(days=8) < end_date:
        alert = st.warning("Max itinerary days allowed are 7. We hope to increase this number over time!")
        time.sleep(3)
        alert.empty()
    if start_date == starter:
        alert = st.warning("Arrival date must be at least one day from today.")
        time.sleep(3)
        alert.empty()
    if start_date == starter + timedelta(days=365):
        alert = st.warning("Arrival date cannot be more than a year from today.")
        time.sleep(3)
        alert.empty() 
    if start_date + timedelta(days=1) == end_date:
        alert = st.warning("There must be at least one day between the arrival and departure day.")
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
                    st.write("No events were found for the day. Try regenerating your itinerary.")
                else:
                    st.subheader(activity['title'])
                    st.image(activity['imageUrl'])
                    st.subheader('Event Description')
                    st.write(activity['description'])
                    st.subheader('Timing')
                    st.write("**Starts at:**", datetime.strptime(activity['startTime'], '%H:%M').strftime("%I:%M %p"))
                    st.write("**Ends at:** ", datetime.strptime(activity['endTime'], '%H:%M').strftime("%I:%M %p"))
                    st.markdown(f'''<a target="_blank" href="{activity["productUrl"]}">
                                <button>
                                    Book this event!
                                </button>
                            </a>''',
                       unsafe_allow_html=True
                        )
        st.balloons()
        st.write('\n\n\n\n')
        st.markdown(f'''<a target="_blank" href="https://docs.google.com/forms/d/e/1FAIpQLSciIVTnEU94L3srZB5xMY3QBREzxNElsZD2rPHhIikD07IbOg/viewform">
                                <button>
                                    Enter your feedback for a chance to win $50!
                                </button>
                            </a>''',
                       unsafe_allow_html=True
                        )
