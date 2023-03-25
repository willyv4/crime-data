from functools import total_ordering
import requests
from config import crime_data_api_key, zipcode_api_key


def get_crime_data(zipcode):

    url = "https://crime-data-by-zipcode-api.p.rapidapi.com/crime_data"

    querystring = {"zip": zipcode}

    headers = {
        "X-RapidAPI-Key": crime_data_api_key,
        "X-RapidAPI-Host": "crime-data-by-zipcode-api.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    return response.json()


def format_data(zipcode):
    data = get_crime_data(zipcode)

    overall_crime = data['Overall']
    crime_specs = data['Crime BreakDown']
    violent_crime_rates = crime_specs[0]
    property_crime_rates = crime_specs[1]
    other_crime_rates = crime_specs[2]

    total_violent = violent_crime_rates["0"]
    total_property = property_crime_rates["0"]
    total_other = other_crime_rates["0"]

    return overall_crime, crime_specs, violent_crime_rates, property_crime_rates, other_crime_rates, total_violent, total_other, total_property


def get_city_data(city, state):

    headers = {
        "apikey": zipcode_api_key
    }

    params = (
        ("city", city),
        ("state_name", state),
        ("country", "us"),
    )

    response = requests.get(
        'https://app.zipcodebase.com/api/v1/code/city', headers=headers, params=params)

    return response.json()


def unpack_zipcode(city, state):
    data = get_city_data(city, state)
    zipcode = data["results"][0]
    return zipcode
