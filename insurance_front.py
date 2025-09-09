import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Category Predictor")
st.markdown("Please Enter Your Details Correctly")

#input field
age = st.number_input("Age", min_value=1, max_value=120, value=35)
weight = st.number_input("Weight (kg)", min_value=1, value=60)
height = st.number_input("Height (m)", min_value=.5, value=1.6)
income_lpa = st.number_input("Annual Income (lpa)", min_value=1, value=10)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
occupation = st.selectbox("Your occupation", options=['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'])

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Insurance Premium Category: **{result['Predicted Category']}**")
        else:
            st.error(f"ApI error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server")