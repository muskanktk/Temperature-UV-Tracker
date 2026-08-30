
import json

import requests
import streamlit as st


lambdaurl = "https://4klf4smujggsy7dk5bhx2yrhye0egbxp.lambda-url.us-east-1.on.aws/"
def getWeatherfromlambda(zipcode):

    response = requests.post(
        lambdaurl,
        json={"zipcode":zipcode}
    )

    response.raise_for_status()

    lambda_response = response.json()

    weatherdata = json.loads(lambda_response["body"])

    return weatherdata

st.title("WEATHER APP")

zipcode = st.text_input("ENTER ZIP CODE...")

if st.button("Get Weather"):
    if zipcode:
        weather = getWeatherfromlambda(zipcode)

        st.subheader("CURRENT WEATHER")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="📍ZIP CODE",
                value=weather["zipcode"]
            )
        with col2:
            st.metric(
                label="🌡️Temperature",
                value=f'{weather["temperature"]:.1f} F'
            )
        with col3:
            st.metric(
                label="☀️UV Index",
                value=weather["uv"]
            )





