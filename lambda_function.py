# AWS lambda/backened

# this lambda function does 
# the part of using zip code to get teh weatehr and uv
# the lambd will send it to the streamlit app

import json
import requests
import os

def getUV(lat, long):

    uv_url = f"https://currentuvindex.com/api/v1/uvi?latitude={lat}&longitude={long}"

    # request a reponse from the url
    reponse = requests.get(uv_url)

    reponse.raise_for_status()

    data = reponse.json()

    uv = data["now"]["uvi"]

    return uv

def CelsiusToFert(temp):
    FTemp = (temp * 9/5) + 32

    return FTemp

def getCoordinates(zipcode):
    ZipcodeInfo = f"https://global.metadapi.com/zipc/v2/zipcodes/{zipcode}"

    API_KEY = os.environ["API_KEY"]

    header = {"Accept": "application/json",
    "Ocp-Apim-Subscription-Key": API_KEY
    }

    #send http request
    response = requests.get(ZipcodeInfo, headers=header)

    response.raise_for_status()

    data = response.json()

    latitude = data["data"][0]["latitude"]
    longitude = data["data"][0]["longitude"]

    
    return latitude,longitude


def EnterZipCode(zipcode):

    # This gets the lat and long using the zipcode
    # calls the function that does it
    latitude, longitude = getCoordinates(zipcode)

    # this is an endpoint and now when calling the
    # API we get the lat and long
    WeatherUrl= f"https://api.weather.gov/points/{latitude},{longitude}"

    # this makes a requrest to the apicall
    response = requests.get(WeatherUrl)

    response.raise_for_status()

    # creates a dictionary to add it
    AreaCode = response.json()

    # this will use the proprties from AreaCode specfically get the
    # forcast of that specfic areacode
    station_url = AreaCode["properties"]["observationStations"]

    # this will make a request to the url for forcast
    response = requests.get(station_url)

    response.raise_for_status()

    stations = response.json()

    station_url = stations["features"][0]["id"]

    observation_url = f"{station_url}/observations/latest"

    response = requests.get(observation_url)
    response.raise_for_status()

    observation = response.json()

    temp = observation["properties"]["temperature"]["value"]

    NewTemp = CelsiusToFert(temp)

    uv = getUV(latitude, longitude)

    return NewTemp, uv

def lambda_handler(event, context):

    if "body" in event: 
        body = json.loads(event["body"])
        zipcode = body["zipcode"]
    # zipcode = event["zipcode"]
    else:
        zipcode = event["zipcode"]

    temp, uv = EnterZipCode(zipcode)

    return {
        "StatusCode": 200,
        "headers": {
            "content-Type": "application/json"
        },
        "body": json.dumps({
             "zipcode": zipcode,
                    "temperature": temp,
                    "uv": uv
        })
    }