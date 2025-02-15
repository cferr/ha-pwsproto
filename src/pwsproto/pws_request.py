import datetime
import logging
from typing import Any, Callable
from homeassistant.const import (
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    PERCENTAGE,
    UnitOfPrecipitationDepth,
    UnitOfIrradiance,
    UV_INDEX,
    CONCENTRATION_PARTS_PER_MILLION,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)

from pwsproto.station import Measurement, WeatherStation


def str_to_int(x: str) -> int:
    return int(x)


def str_to_float(x: str) -> float:
    return float(x)


def identity(x: str) -> str:
    return x


class ParameterConversion:
    def __init__(
        self,
        sensor_name: str,
        converter: Callable[[str], Any],
        reported_unit: str | None = None,
    ):
        self.sensor_name = sensor_name
        self.converter = converter
        self.reported_unit = reported_unit

    def convert(self, value: str):
        return Measurement(value=self.converter(value), unit=self.reported_unit)


# Reference: https://support.weather.com/s/article/PWS-Upload-Protocol?language=en_US
url_param_to_status_dict: dict[str, ParameterConversion] = {
    # Generic fields
    "dateutc": ParameterConversion(
        "date",
        lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S"),
    ),
    "softwaretype": ParameterConversion("software_type", identity),
    # Wind
    "winddir": ParameterConversion("wind_direction", identity, "wind_direction"),
    "windspeedmph": ParameterConversion(
        "wind_speed",
        str_to_float,
        reported_unit=UnitOfSpeed.MILES_PER_HOUR,
    ),
    "windgustmph": ParameterConversion(
        "wind_gust_speed",
        str_to_float,
        reported_unit=UnitOfSpeed.MILES_PER_HOUR,
    ),
    "windgustdir": ParameterConversion(
        "wind_gust_direction", identity, "wind_direction"
    ),
    "windspdmph_avg2m": ParameterConversion(
        "wind_speed_avg_2m",
        str_to_float,
        reported_unit=UnitOfSpeed.MILES_PER_HOUR,
    ),
    "winddir_avg2m": ParameterConversion(
        "wind_direction_avg_2m", str_to_float, "wind_direction"
    ),
    "windgustmph_10m": ParameterConversion(
        "wind_gust_speed_10m",
        str_to_float,
        reported_unit=UnitOfSpeed.MILES_PER_HOUR,
    ),
    "windgustdir_10m": ParameterConversion(
        "wind_gust_direction_10m", identity, "wind_direction"
    ),
    # Outdoor temperature/pressure/humidity
    "humidity": ParameterConversion(
        "outdoor_humidity",
        str_to_float,
        reported_unit=PERCENTAGE,
    ),
    "dewptf": ParameterConversion(
        "dew_temperature",
        str_to_float,
        reported_unit=UnitOfTemperature.FAHRENHEIT,
    ),
    "tempf": ParameterConversion(
        "outdoor_temperature",
        str_to_float,
        reported_unit=UnitOfTemperature.FAHRENHEIT,
    ),
    # * for extra outdoor sensors use temp2f, temp3f, and so on
    "baromin": ParameterConversion(
        "barometric_pressure",
        str_to_float,
        reported_unit=UnitOfPressure.INHG,
    ),
    # General weather info (text)
    "weather": ParameterConversion("weather_text", identity),
    "clouds": ParameterConversion("clouds", identity),
    # Soil
    "soiltempf": ParameterConversion(
        "soil_temperature",
        str_to_float,
        reported_unit=UnitOfTemperature.FAHRENHEIT,
    ),
    # * for sensors 2,3,4 use soiltemp2f, soiltemp3f, and soiltemp4f
    "soilmoisture": ParameterConversion(
        "soil_moisture",
        str_to_float,
        reported_unit=PERCENTAGE,
    ),
    # * for sensors 2,3,4 use soilmoisture2, soilmoisture3, and soilmoisture4
    "leafwetness": ParameterConversion(
        "leaf_wetness",
        str_to_float,
        reported_unit=PERCENTAGE,
    ),
    # + for sensor 2 use leafwetness2
    # Sunlight
    "solarradiation": ParameterConversion(
        "solar_radiation",
        str_to_float,
        reported_unit=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
    ),
    "UV": ParameterConversion("uv_index", str_to_int, reported_unit=UV_INDEX),
    "visibility": ParameterConversion("nm_visibility", identity),
    # Rain
    "rainin": ParameterConversion(
        "rain_hourly",
        str_to_float,
        reported_unit=UnitOfPrecipitationDepth.INCHES,
    ),
    "dailyrainin": ParameterConversion(
        "rain_daily",
        str_to_float,
        reported_unit=UnitOfPrecipitationDepth.INCHES,
    ),
    # Indoor sensors
    "indoortempf": ParameterConversion(
        "indoor_temperature",
        str_to_float,
        reported_unit=UnitOfTemperature.FAHRENHEIT,
    ),
    "indoorhumidity": ParameterConversion(
        "indoor_humidity",
        str_to_float,
        reported_unit=PERCENTAGE,
    ),
    # Air quality
    "AqNO": ParameterConversion(
        "pollution_no", str_to_int, reported_unit=CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNO2T": ParameterConversion(
        "pollution_no2t", str_to_int, reported_unit=CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNO2": ParameterConversion(
        "pollution_no2", str_to_int, reported_unit=CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNO2Y": ParameterConversion(
        "pollution_no2y", str_to_int, reported_unit=CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNOX": ParameterConversion(
        "pollution_nox", str_to_int, reported_unit=CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNOY": ParameterConversion(
        "pollution_noy", str_to_int, reported_unit=CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNO3": ParameterConversion(
        "pollution_no3_ion",
        str_to_float,
        reported_unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqSO4": ParameterConversion(
        "pollution_so4_ion",
        str_to_float,
        reported_unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqSO2": ParameterConversion(
        "pollution_sulfur_dioxide",
        str_to_int,
        reported_unit=CONCENTRATION_PARTS_PER_BILLION,
    ),
    "AqSO2T": ParameterConversion(
        "pollution_sulfur_dioxide_trace",
        str_to_int,
        reported_unit=CONCENTRATION_PARTS_PER_BILLION,
    ),
    "AqCO": ParameterConversion(
        "pollution_carbon_monoxide",
        str_to_int,
        reported_unit=CONCENTRATION_PARTS_PER_MILLION,
    ),
    "AqCOT": ParameterConversion(
        "pollution_carbon_monoxide_trace",
        str_to_int,
        reported_unit=CONCENTRATION_PARTS_PER_BILLION,
    ),
    "AqEC": ParameterConversion(
        "pollution_elemental_carbon",
        str_to_float,
        reported_unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqOC": ParameterConversion(
        "pollution_organic_carbon",
        str_to_float,
        reported_unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqBC": ParameterConversion(
        "pollution_black_carbon",
        str_to_float,
        reported_unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqUV": ParameterConversion(
        "pollution_uv_aeth",
        str_to_float,
        reported_unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqPM2.5": ParameterConversion(
        "pollution_pm25_mass",
        str_to_float,
        reported_unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqPM10": ParameterConversion(
        "pollution_pm10_mass",
        str_to_float,
        reported_unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqOZONE": ParameterConversion(
        "pollution_ozone", str_to_int, reported_unit=CONCENTRATION_PARTS_PER_BILLION
    ),
}


def _pws_to_measurement_dict(fields: dict[str, str]) -> dict[str, Measurement]:
    measurement_dict: dict[str, Measurement] = {}
    for given_param, value in fields.items():
        param_matched = False
        for expected_param in url_param_to_status_dict:
            if given_param == expected_param:
                param_matched = True
                converter = url_param_to_status_dict[expected_param]
                try:
                    converted_value = converter.convert(value)
                    measurement_dict[converter.sensor_name] = converted_value
                except ValueError as err:
                    logging.warning(f"Parameter error for {given_param}: {err}")
                    pass
                break
        if not param_matched:
            logging.warning(f"Unknown parameter: {given_param}")

    return measurement_dict


class PWSRequestProcessor:
    def __init__(
        self,
        stations: list[WeatherStation],
    ):
        self.stations = stations

    def process_request(self, params: dict[str, str]) -> None:
        # Grab ID, password
        if "ID" not in params or "PASSWORD" not in params:
            raise NotImplementedError

        id = params["ID"]
        password = params["PASSWORD"]

        stations_auth = list(
            filter(
                lambda station: station.id == id and station.password == password,
                self.stations,
            )
        )

        if len(stations_auth) == 0:
            raise PermissionError("Invalid station ID/password")

        params_filtered = {
            key: value for key, value in params.items() if key not in ["ID", "PASSWORD"]
        }
        measurement_dict = _pws_to_measurement_dict(params_filtered)

        for station in stations_auth:
            station.update_measurement(measurement_dict)
