"""
This module contains functions to fetch weather data from two sources: 
    the OpenWeatherMap API and the BME280 sensor.

Functions:
    __open_weather_api(latitude,longitude,key): 
        Fetches weather data from the OpenWeatherMap API.
    __bme_280(port, address): 
        Fetches weather data from the BME280 sensor.

The __open_weather_api function takes in latitude, longitude, and an API key, 
and returns a tuple containing the temperature, pressure, and humidity at 
the specified location.

The __bme_280 function takes in a port and an address, and returns a tuple 
containing the temperature, pressure, and humidity from the BME280 sensor 
connected at the specified port and address.
"""

import argparse
import csv
import io
import os
from datetime import datetime

import bme280
import requests
import smbus2
from meteocalc import dew_point


def __open_weather_api(latitude, longitude, key):
    """
    Fetches weather data from the OpenWeatherMap API.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        key (str): The API key for OpenWeatherMap.

    Returns:
        tuple: The temperature, pressure, and humidity at the location.
    """
    call = "https://api.openweathermap.org/data/2.5/weather?"
    location_part = f"lat={latitude}&lon={longitude}"
    api = f"{call}{location_part}&appid={key}&units=metric"
    response = requests.get(api, timeout=10)
    json_data = response.json()
    return (
        json_data["main"]["temp"],
        json_data["main"]["pressure"],
        json_data["main"]["humidity"],
    )


def __bme_280(address):
    """
    Fetches weather data from the BME280 sensor.

    Args:
        address (str): The address of the sensor.

    Returns:
        tuple: The temperature, pressure, and humidity from the sensor.
    """
    bus = smbus2.SMBus(1)
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)

    return round(data.temperature, 2), round(data.pressure, 2), round(data.humidity, 2)


def get_data(api, lat, lon, file_location, address):
    """
    Fetches weather data and writes it to a file.

    Args:
        api (str): The API key for OpenWeatherMap.
                If this is None, data is fetched from the BME280 sensor.
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.
        file_location (str): The location of the file to which the data is written.
        address (str): The address of the BME280 sensor.
    """
    if api:
        temperature, pressure, humidity = __open_weather_api(lat, lon, api)
    else:
        temperature, pressure, humidity = __bme_280(address)

    formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    get_dew_point = round(dew_point(temperature, humidity), 2)
    with io.open(file_location, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if os.stat(file_location).st_size == 0:
            writer.writerow(
                ["date-time", "temperature", "pressure", "humidity", "dew-point"]
            )
        writer.writerow(
            [formatted_date, temperature, pressure, humidity, get_dew_point]
        )


def __parse_args():
    """
    Parses command line arguments.

    This function uses argparse to parse command line arguments and returns an argparse.

    Returns:
        argparse.Namespace: An object that holds the command line arguments as attributes.
            This object will have the following attributes:
            - api (str): The API key for OpenWeatherMap.
            - lat (float): The latitude for weather data.
            - lon (float): The longitude for weather data.
            - file (str): The file location for output.
            - port (int): The port for the BME280 sensor.
            - address (str): The address for the BME280 sensor.
    """
    parser = argparse.ArgumentParser(description="Environment Checker")
    parser.add_argument(
        "--api", type=str, required=False, help="API key for OpenWeatherMap"
    )
    parser.add_argument(
        "--lat", type=float, required=False, help="Latitude for weather data"
    )
    parser.add_argument(
        "--lon", type=float, required=False, help="Longitude for weather data"
    )
    parser.add_argument(
        "--file", type=str, required=False, help="File location for output"
    )
    parser.add_argument(
        "--address",
        type=str,
        required=False,
        default="0x77",
        help="Address for BME280 sensor",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = __parse_args()
    get_data(args.api, args.lat, args.lon, args.file, args.address)
