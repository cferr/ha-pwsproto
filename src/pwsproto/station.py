from dataclasses import dataclass
import datetime
from typing import Callable, Any
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
import logging


def str_to_int(x: str) -> int:
    return int(x)


def str_to_float(x: str) -> float:
    return float(x)


def identity(x: str) -> str:
    return x


class Measurement:
    def __init__(
        self, value: Any, unit: str | None = None, device_class: str | None = None
    ):
        self.value = value
        self.unit = unit
        self.device_class = device_class


class UrlConversion:
    def __init__(
        self,
        name: str,
        fn: Callable[[str], Any],
        device_class: str | None = None,
        unit: str | None = None,
    ):
        self.name = name
        self.fn = fn
        self.device_class = device_class
        self.unit = unit

    def __call__(self, param: str):
        return Measurement(
            self.fn(param), unit=self.unit, device_class=self.device_class
        )


# Reference: https://support.weather.com/s/article/PWS-Upload-Protocol?language=en_US
url_to_status_dict: dict[str, UrlConversion] = {
    # Generic fields
    "dateutc": UrlConversion(
        "date", lambda s: datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S"), "date"
    ),
    "softwaretype": UrlConversion("software_type", identity),
    # Wind
    "winddir": UrlConversion("wind_direction", identity, "wind_direction"),
    "windspeedmph": UrlConversion(
        "wind_speed", str_to_float, "wind_speed", UnitOfSpeed.MILES_PER_HOUR
    ),
    "windgustmph": UrlConversion(
        "wind_gust_speed", str_to_float, "wind_speed", UnitOfSpeed.MILES_PER_HOUR
    ),
    "windgustdir": UrlConversion("wind_gust_direction", identity, "wind_direction"),
    "windspdmph_avg2m": UrlConversion(
        "wind_speed_avg_2m", str_to_float, "wind_speed", UnitOfSpeed.MILES_PER_HOUR
    ),
    "winddir_avg2m": UrlConversion(
        "wind_direction_avg_2m", str_to_float, "wind_direction"
    ),
    "windgustmph_10m": UrlConversion(
        "wind_gust_speed_10m", str_to_float, "wind_speed", UnitOfSpeed.MILES_PER_HOUR
    ),
    "windgustdir_10m": UrlConversion(
        "wind_gust_direction_10m", identity, "wind_direction"
    ),
    # Outdoor temperature/pressure/humidity
    "humidity": UrlConversion("outdoor_humidity", str_to_float, "humidity", PERCENTAGE),
    "dewptf": UrlConversion(
        "dew_temperature", str_to_float, "temperature", UnitOfTemperature.FAHRENHEIT
    ),
    "tempf": UrlConversion(
        "outdoor_temperature", str_to_float, "temperature", UnitOfTemperature.FAHRENHEIT
    ),
    # * for extra outdoor sensors use temp2f, temp3f, and so on
    "baromin": UrlConversion(
        "barometric_pressure", str_to_float, "pressure", UnitOfPressure.INHG
    ),
    # General weather info (text)
    "weather": UrlConversion("weather_text", identity),
    "clouds": UrlConversion("clouds", identity),
    # Soil
    "soiltempf": UrlConversion(
        "soil_temperature", str_to_float, "temperature", UnitOfTemperature.FAHRENHEIT
    ),
    # * for sensors 2,3,4 use soiltemp2f, soiltemp3f, and soiltemp4f
    "soilmoisture": UrlConversion(
        "soil_moisture", str_to_float, "moisture", PERCENTAGE
    ),
    # * for sensors 2,3,4 use soilmoisture2, soilmoisture3, and soilmoisture4
    "leafwetness": UrlConversion("leaf_wetness", str_to_float, "moisture", PERCENTAGE),
    # + for sensor 2 use leafwetness2
    # Sunlight
    "solarradiation": UrlConversion(
        "solar_radiation",
        str_to_float,
        "irradiance",
        UnitOfIrradiance.WATTS_PER_SQUARE_METER,
    ),
    "UV": UrlConversion("uv_index", str_to_int, None, UV_INDEX),
    "visibility": UrlConversion("nm_visibility", identity),
    # Rain
    "rainin": UrlConversion(
        "rain_hourly", str_to_float, "precipitation", UnitOfPrecipitationDepth.INCHES
    ),
    "dailyrainin": UrlConversion(
        "rain_daily", str_to_float, "precipitation", UnitOfPrecipitationDepth.INCHES
    ),
    # Indoor sensors
    "indoortempf": UrlConversion(
        "indoor_temperature", str_to_float, "temperature", UnitOfTemperature.FAHRENHEIT
    ),
    "indoorhumidity": UrlConversion(
        "indoor_humidity", str_to_float, "humidity", PERCENTAGE
    ),
    # Air quality
    "AqNO": UrlConversion("pollution_no", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqNO2T": UrlConversion(
        "pollution_no2t", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNO2": UrlConversion(
        "pollution_no2", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNO2Y": UrlConversion(
        "pollution_no2y", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNOX": UrlConversion(
        "pollution_nox", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNOY": UrlConversion(
        "pollution_noy", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqNO3": UrlConversion(
        "pollution_no3_ion", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    ),
    "AqSO4": UrlConversion(
        "pollution_so4_ion", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    ),
    "AqSO2": UrlConversion(
        "pollution_sulfur_dioxide", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqSO2T": UrlConversion(
        "pollution_sulfur_dioxide_trace", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqCO": UrlConversion(
        "pollution_carbon_monoxide", str_to_int, CONCENTRATION_PARTS_PER_MILLION
    ),
    "AqCOT": UrlConversion(
        "pollution_carbon_monoxide_trace", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
    "AqEC": UrlConversion(
        "pollution_elemental_carbon",
        str_to_float,
        CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqOC": UrlConversion(
        "pollution_organic_carbon",
        str_to_float,
        CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "AqBC": UrlConversion(
        "pollution_black_carbon", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    ),
    "AqUV": UrlConversion(
        "pollution_uv_aeth", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    ),
    "AqPM2.5": UrlConversion(
        "pollution_pm25_mass", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    ),
    "AqPM10": UrlConversion("pollution_pm10_mass", str_to_float),
    "AqOZONE": UrlConversion(
        "pollution_ozone", str_to_int, CONCENTRATION_PARTS_PER_BILLION
    ),
}


def _pws_to_measurement_dict(fields: dict[str, str]) -> dict[str, Measurement]:
    measurement_dict: dict[str, Measurement] = {}
    for given_param, value in fields.items():
        param_matched = False
        for expected_param in url_to_status_dict:
            if given_param == expected_param:
                param_matched = True
                converter = url_to_status_dict[expected_param]
                try:
                    converted_value = converter(value)
                    measurement_dict[converter.name] = converted_value
                except ValueError as err:
                    logging.warning(f"Parameter error for {given_param}: {err}")
                    pass
                break
        if not param_matched:
            logging.warning(f"Unknown parameter: {given_param}")

    return measurement_dict


@dataclass
class WeatherStation:
    id: str
    password: str
    update_callback: Callable[["WeatherStation"], None] | None

    def __init__(
        self,
        id: str,
        password: str,
        update_callback: Callable[["WeatherStation"], None] | None = None,
    ):
        self.id = id
        self.password = password
        self.update_callback = update_callback

    latest_measurement: dict[str, Measurement] | None = None

    def update_measurement_from_pws_params(self, raw_pws_params: dict[str, str]):
        self.latest_measurement = _pws_to_measurement_dict(raw_pws_params)
        if self.update_callback is not None:
            self.update_callback(self)

    def get_ha_payloads(self) -> dict[str, dict[str, Any]]:
        if self.latest_measurement is None:
            raise ValueError("No measurement")
        assert self.latest_measurement is not None

        if "date" not in self.latest_measurement:
            raise ValueError("Date absent from measurement")

        latest_measurement_date: datetime.datetime = self.latest_measurement[
            "date"
        ].value

        payloads = {}

        for name, measurement in self.latest_measurement.items():
            # Do not generate a payload for the date
            if name == "date":
                continue

            attributes = {}
            if measurement.unit is not None:
                attributes["unit_of_measurement"] = measurement.unit
            if measurement.device_class is not None:
                attributes["device_class"] = measurement.device_class
            attributes["friendly_name"] = name
            attributes["updated"] = str(
                latest_measurement_date.strftime("%Y-%m-%dT%H:%M:%S%z")
            )
            payload = {"state": str(measurement.value), "attributes": attributes}

            payloads[name] = payload

        return payloads
