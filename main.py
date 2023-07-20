import streamlit as st
import json
import requests
import extractor
import openai
import datetime
import tag_lib
import base64
import integrations
import availability


with open('english_tags.json') as file:
        tags_data = json.load(file)


st.set_page_config(
    page_title="travlgo",
    page_icon="travlgo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.image("travlgo.png", use_column_width=True)

st.title('Welcome to travlgo!')
text_header = 'Please enter in the information below for an optimized experience.'
st.markdown(f'<p style="color:#000000;font-size:20px;border-radius:2%;">{text_header}</p>', unsafe_allow_html=True)

global submitted

col1, col2, col3 = st.columns(3)

with st.form("my_form"):
    with col1:
        initial_destination = st.text_input('**Destination**')
        start_date = st.date_input('**Depart Date**')
        adults = st.number_input('**Number of Adults**', min_value=0)
    with col2:
        optional_destination = st.text_input('**Additional Destination** (optional)', ' ')
        end_date = st.date_input('**Return Date**')
        children = st.number_input('**Number of Children**', min_value=0)
        

    with col3:
        budget = st.number_input('**Budget**', min_value=0, step=10)
        time = st.selectbox(
        '**Time of Arrival**',
        ('Select below', 'Morning', 'Afternoon', 'Evening'))

        
    travel_pace = st.select_slider('**Your Travel Intensity**', options = ['Slow', 'Medium', 'Fast'])

    Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: rgb(14, 38, 74); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)

        
    Slider_Number = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div > div
                                    { color: rgb(14, 38, 74); } </style>''', unsafe_allow_html = True) 
     
    
    user_tags = st.multiselect(
    '**Customize Your Trip**', options = tag_lib.snatch_tags)
    # Every form must have a submit button.
    submitted = st.form_submit_button('Submit')
    if submitted:
        dates = availability.get_dates_in_between(start_date, end_date)
        with st.spinner('Wait for it...'):
            calendar = integrations.itinerary_creation(destination=initial_destination, start_date=start_date, end_date=end_date, user_tags=user_tags, event_number=20)
            st.success('Success!', icon="✅")
            for index, days in enumerate(calendar):
                st.header(dates[index])
                for activity in days:
                    if "No found event for the day" in activity:
                        st.write("No event found for the day")
                    else:
                        st.subheader(activity['title'])
                        st.image(activity['imageUrl'])
                        st.write(activity['description'])
                        st.write("Starts at ", activity['startTime'])
                        st.write("Ends at: ", activity['endTime'])
                        st.write(f'''
                            <a target="_self" href="{activity["productUrl"]}">
                                <button>
                                    Book this event!
                                </button>
                            </a>
                            ''',
                            unsafe_allow_html=True
                        )
                        st.write("\n\n")
            st.balloons()

            