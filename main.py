import streamlit as st
import time


""""""
st.title('Welcome to travlgo!')

with st.form("my_form"):
    destination = st.text_input('Final Destination:', 'Paris')
    budget = st.number_input('Budget:', min_value=0, step=10)
    arrival_date = st.date_input("Arrival Date:")
    departure_date = st.date_input("Departure Date:")
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        with st.spinner('Wait for it...'):
            time.sleep(5)
            st.success('Done!')
