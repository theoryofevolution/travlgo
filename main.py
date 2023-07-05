import streamlit as st

st.title('Welcome to travlgo!')

destination = st.text_input('Final Destination:', 'Paris')
budget = st.number_input('Budget:', min_value=0, step=10)
arrival_date = st.date_input("Arrival Date:")
departure_date = st.date_input("Departure Date:")