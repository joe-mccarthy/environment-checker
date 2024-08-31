import argparse
from unittest.mock import patch, MagicMock, mock_open
from src.environment.environment_checker import (
    __parse_args,
    __open_weather_api,
    __bme_280,
    get_data,
)
import math


@patch("requests.get")
def test_open_weather_api(mock_get):
    # Mock the response from the API
    mock_response = {"main": {"temp": 25.5, "pressure": 1013, "humidity": 70}}
    mock_get.return_value.json.return_value = mock_response

    # Call the function with sample latitude, longitude, and API key
    temperature, pressure, humidity = __open_weather_api(
        37.7749, -122.4194, "your-api-key"
    )

    # Assert that the function returns the expected values
    assert math.isclose(temperature, 25.5)
    assert math.isclose(pressure, 1013)
    assert math.isclose(humidity, 70)


@patch("smbus2.SMBus")
@patch("bme280.load_calibration_params")
@patch("bme280.sample")
def test_bme_280(mock_sample, mock_load_calibration_params, mock_smbus):
    # Arrange
    mock_load_calibration_params.return_value = MagicMock()
    mock_sample.return_value.temperature = 20.0
    mock_sample.return_value.pressure = 1000.0
    mock_sample.return_value.humidity = 50.0
    address = 0x77

    # Act
    temperature, pressure, humidity = __bme_280(address)

    # Assert
    mock_smbus.assert_called_once_with(1)
    mock_load_calibration_params.assert_called_once_with(
        mock_smbus.return_value, address
    )
    mock_sample.assert_called_once_with(
        mock_smbus.return_value, address, mock_load_calibration_params.return_value
    )

    assert math.isclose(temperature, 20.0)
    assert math.isclose(pressure, 1000.0)
    assert math.isclose(humidity, 50.0)


@patch("requests.get")
@patch("src.environment.environment_checker.os.stat")
def test_get_data_api(mock_stat, mock_api):
    mock_response = {"main": {"temp": 25.5, "pressure": 1013, "humidity": 70}}
    mock_api.return_value.json.return_value = mock_response
    mock_stat.return_value.st_size = 0
    mock_file = mock_open()
    with patch("src.environment.environment_checker.io.open", mock_file, create=True):
        get_data("api_key", "lat", "lon", "file_location", "address")
    mock_file.assert_called_once_with(
        "file_location", "a", newline="", encoding="utf-8"
    )


@patch("smbus2.SMBus")
@patch("bme280.load_calibration_params")
@patch("bme280.sample")
@patch("src.environment.environment_checker.os.stat")
def test_get_data_bme(mock_stat, mock_sample, mock_load_calibration_params, mock_smbus):
    # Arrange
    mock_load_calibration_params.return_value = MagicMock()
    mock_sample.return_value.temperature = 20.0
    mock_sample.return_value.pressure = 1000.0
    mock_sample.return_value.humidity = 50.0
    mock_file = mock_open()
    mock_stat.return_value.st_size = 0

    with patch("src.environment.environment_checker.io.open", mock_file, create=True):
        get_data(None, "lat", "lon", "file_location", "address")
        mock_file.assert_called_once_with(
            "file_location", "a", newline="", encoding="utf-8"
        )


@patch("argparse.ArgumentParser.parse_args")
def test_parse_args(mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        api="api_key", lat=1.0, lon=1.0, file="file_location", port=1, address="0x77"
    )
    result = __parse_args()
    assert result.api == "api_key"
    assert math.isclose(result.lat, 1.0)
    assert math.isclose(result.lon, 1.0)
    assert result.file == "file_location"
    assert result.port == 1
    assert result.address == "0x77"
