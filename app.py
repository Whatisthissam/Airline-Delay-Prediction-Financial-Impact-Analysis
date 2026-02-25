import streamlit as st
import numpy as np
import joblib

st.title("✈️ Airline Delay Prediction & Financial Impact")

st.write("Predict arrival delay and estimate financial loss.")

# User Inputs
distance = st.number_input("Enter Flight Distance (in miles):", min_value=0.0)
departure_delay = st.number_input("Enter Departure Delay (in minutes):", min_value=0.0)

# Simple prediction logic (since model not saved separately)
# Using basic assumption: arrival delay highly depends on departure delay

if st.button("Predict"):
    predicted_arrival_delay = departure_delay * 0.9 + (distance * 0.001)

    cost_per_minute = 100
    financial_loss = predicted_arrival_delay * cost_per_minute

    st.success(f"Predicted Arrival Delay: {predicted_arrival_delay:.2f} minutes")
    st.error(f"Estimated Financial Loss: ₹ {financial_loss:.2f}")
