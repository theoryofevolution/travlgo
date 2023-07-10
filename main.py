import streamlit as st
import integrations
import tag_lib

st.title('Welcome to travlgo!')
global submitted
with st.form("my_form"):

    destination = st.text_input('Final Destination:', 'Paris')
    budget = st.number_input('Budget:', min_value=0, step=10)
    start_date = st.date_input("Arrival Date:")
    end_date = st.date_input("Departure Date:")
    user_tags = st.multiselect(
    'Customize your trip', options = tag_lib.snatch_tags)
    travel_pace = st.select_slider(
    'Select your travel intensity',
    options=['Slow', 'Medium', 'Fast'])
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner('Wait for it...'):
        extracted_values = integrations.viator_post_request(destination=destination, start_date=start_date, end_date=end_date, user_tags=user_tags, event_number=10)
        itinerary = integrations.gpt_formatting(extracted_values, start_date, end_date)
        st.text(itinerary)
        for values in extracted_values:
            st.write(values['productUrl'])