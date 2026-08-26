# import streamlit as st
# # help makes request through http calls
# # to get information using API calls
import json

import requests
import streamlit as st
# import pgeocode 
# import sys
# import json
# def getUV(lat, long):

#     uv_url = f"https://currentuvindex.com/api/v1/uvi?latitude={lat}&longitude={long}"

#     # request a reponse from the url
#     reponse = requests.get(uv_url)

#     reponse.raise_for_status()

#     data = reponse.json()

#     uv = data["now"]["uvi"]

#     return uv

# def CelsiusToFert(temp):
#     FTemp = (temp * 9/5) + 32

#     return FTemp

# def getCoordinates(zipcode):
#     ZipcodeInfo = f"https://global.metadapi.com/zipc/v2/zipcodes/{zipcode}"

#     API_KEY = st.secrets["API_KEY"]

#     header = {"Accept": "application/json",
#     "Ocp-Apim-Subscription-Key": API_KEY
#     }

#     #send http request
#     response = requests.get(ZipcodeInfo, headers=header)

#     response.raise_for_status()

#     data = response.json()

#     latitude = data["data"][0]["latitude"]
#     longitude = data["data"][0]["longitude"]

    
#     return latitude,longitude


# def EnterZipCode(zipcode):

#     # This gets the lat and long using the zipcode
#     # calls the function that does it
#     latitude, longitude = getCoordinates(zipcode)

#     # this is an endpoint and now when calling the
#     # API we get the lat and long
#     WeatherUrl= f"https://api.weather.gov/points/{latitude},{longitude}"

#     # this makes a requrest to the apicall
#     response = requests.get(WeatherUrl)

#     response.raise_for_status()

#     # creates a dictionary to add it
#     AreaCode = response.json()

#     # this will use the proprties from AreaCode specfically get the
#     # forcast of that specfic areacode
#     station_url = AreaCode["properties"]["observationStations"]

#     # this will make a request to the url for forcast
#     response = requests.get(station_url)

#     response.raise_for_status()

#     stations = response.json()

#     station_url = stations["features"][0]["id"]

#     observation_url = f"{station_url}/observations/latest"

#     response = requests.get(observation_url)
#     response.raise_for_status()

#     observation = response.json()

#     temp = observation["properties"]["temperature"]["value"]

#     NewTemp = CelsiusToFert(temp)

#     uv = getUV(latitude, longitude)

#     return NewTemp, uv

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





# if __name__ == "__main__":

#     if  len(sys.argv) < 2:
#         print("Enter zipcode")
#         sys.exit()

#     zipcode = sys.argv[1]

#     print("ZIP CODE:", zipcode)

#     weather = getWeatherfromlambda(zipcode)

#     temp = weather["temperature"]
#     uv = weather["uv"]

#     print("Current Temperature:", temp)
#     print("UV:", uv)



