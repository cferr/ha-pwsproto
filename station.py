from dataclasses import dataclass, asdict, fields
import datetime
from typing import Callable, Any
from homeassistant.const import UnitOfPressure, UnitOfLength, UnitOfSpeed, UnitOfTemperature, PERCENTAGE, UnitOfPrecipitationDepth, UnitOfIrradiance, UV_INDEX, CONCENTRATION_PARTS_PER_MILLION, CONCENTRATION_PARTS_PER_BILLION, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

str_to_int = lambda x : int(x)
str_to_float = lambda x : float(x)
identity = lambda x : x

class UrlConversion:
    def __init__(self, name: str, fn : Callable[str, Any], unit: str | None = None):
        self.name = name
        self.fn = fn
        self.unit = unit
    
    def __call__(self, param : str):
        return self.fn(param)

url_to_status_dict: dict[str, UrlConversion] = {
    "dateutc": UrlConversion("date", lambda s : datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")),
    "winddir": UrlConversion("wind_direction", identity),
    "windspeedmph": UrlConversion("wind_speed", str_to_float, UnitOfSpeed.MILES_PER_HOUR),
    "windgustmph": UrlConversion("wind_gust_speed", str_to_float, UnitOfSpeed.MILES_PER_HOUR),
    "windgustdir": UrlConversion("wind_gust_direction", identity),
    "windspdmph_avg2m": UrlConversion("wind_speed_avg_2m", str_to_float, UnitOfSpeed.MILES_PER_HOUR),
    "winddir_avg2m": UrlConversion("wind_direction_avg_2m", str_to_float, UnitOfSpeed.MILES_PER_HOUR),
    "windgustmph_10m": UrlConversion("wind_gust_speed_10m", str_to_float, UnitOfSpeed.MILES_PER_HOUR),
    "windgustdir_10m": UrlConversion("wind_gust_direction_10m", identity),
    "humidity": UrlConversion("outdoor_humidity", str_to_float, PERCENTAGE),
    "dewptf": UrlConversion("dew_temperature", str_to_float, UnitOfTemperature.FAHRENHEIT),
    "tempf": UrlConversion("outdoor_temperature", str_to_float, UnitOfTemperature.FAHRENHEIT),
    # * for extra outdoor sensors use temp2f, temp3f, and so on
    "rainin": UrlConversion("rain_hourly", str_to_float, UnitOfPrecipitationDepth.INCHES),
    "dailyrainin": UrlConversion("rain_daily", str_to_float, UnitOfPrecipitationDepth.INCHES),
    "baromin": UrlConversion("barometric_pressure", str_to_float, UnitOfPressure.INHG),
    "weather": UrlConversion("weather_text", identity),
    "clouds": UrlConversion("clouds", identity),
    "soiltempf": UrlConversion("soil_temperature", str_to_float, UnitOfTemperature.FAHRENHEIT),
    # * for sensors 2,3,4 use soiltemp2f, soiltemp3f, and soiltemp4f
    "soilmoisture": UrlConversion("soil_moisture", str_to_float, PERCENTAGE),
    # * for sensors 2,3,4 use soilmoisture2, soilmoisture3, and soilmoisture4
    "leafwetness": UrlConversion("leaf_wetness", str_to_float, PERCENTAGE),
    # + for sensor 2 use leafwetness2
    "solarradiation": UrlConversion("solar_radiation", str_to_float, UnitOfIrradiance.WATTS_PER_SQUARE_METER),
    "UV": UrlConversion("uv_index", str_to_int, UV_INDEX),
    "visibility": UrlConversion("nm_visibility", identity),
    "indoortempf": UrlConversion("indoor_temperature", str_to_float, UnitOfTemperature.FAHRENHEIT),
    "indoorhumidity": UrlConversion("indoor_humidity", str_to_float, PERCENTAGE),
    # Pollution Fields:
    "AqNO": UrlConversion("pollution_no", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqNO2T": UrlConversion("pollution_no2t", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqNO2": UrlConversion("pollution_no2", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqNO2Y": UrlConversion("pollution_no2y", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqNOX": UrlConversion("pollution_nox", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqNOY": UrlConversion("pollution_noy", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqNO3": UrlConversion("pollution_no3_ion", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
    "AqSO4": UrlConversion("pollution_so4_ion", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
    "AqSO2": UrlConversion("pollution_sulfur_dioxide", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqSO2T": UrlConversion("pollution_sulfur_dioxide_trace", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqCO": UrlConversion("pollution_carbon_monoxide", str_to_int, CONCENTRATION_PARTS_PER_MILLION),
    "AqCOT": UrlConversion("pollution_carbon_monoxide_trace", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "AqEC": UrlConversion("pollution_elemental_carbon", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
    "AqOC": UrlConversion("pollution_organic_carbon", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
    "AqBC": UrlConversion("pollution_black_carbon", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
    "AqUV": UrlConversion("pollution_uv_aeth", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
    "AqPM2.5": UrlConversion("pollution_pm25_mass", str_to_float, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER),
    "AqPM10": UrlConversion("pollution_pm10_mass", str_to_float),
    "AqOZONE": UrlConversion("pollution_ozone", str_to_int, CONCENTRATION_PARTS_PER_BILLION),
    "softwaretype": UrlConversion("software_type", identity),
}


@dataclass
class Measurement:
    date: datetime.datetime | None = None
    # Wind
    wind_direction: int | None = None
    wind_speed: int | None = None
    wind_gust_speed: int | None = None
    wind_gust_direction: int | None = None
    wind_speed_avg_2m: int | None = None
    wind_direction_avg_2m: int | None = None
    wind_gust_speed_10m: int | None = None
    wind_gust_direction_10m: int | None = None
    # Outdoor sensor
    outdoor_humidity: int | None = None
    dew_temperature: int | None = None
    outdoor_temperature: int | None = None
    # Rain
    rain_hourly: int | None = None
    rain_daily: int | None = None
    # Pressure
    barometric_pressure: int | None = None
    # Synthetic
    weather_text: int | None = None
    clouds: int | None = None
    # Soil
    soil_temperature: int | None = None
    soil_moisture: int | None = None
    leaf_wetness: int | None = None
    # Sun
    solar_radiation: int | None = None
    uv_index: int | None = None
    nm_visibility: int | None = None
    # Indoor
    indoor_temperature: int | None = None
    indoor_humidity: int | None = None
    # Pollution
    pollution_no: int | None = None
    pollution_no2t: int | None = None
    pollution_no2: int | None = None
    pollution_no2y: int | None = None
    pollution_nox: int | None = None
    pollution_noy: int | None = None
    pollution_no3_ion: int | None = None
    pollution_so4_ion: int | None = None
    pollution_sulfur_dioxide: int | None = None
    pollution_sulfur_dioxide_trace: int | None = None
    pollution_carbon_monoxide: int | None = None
    pollution_carbon_monoxide_trace: int | None = None
    pollution_elemental_carbon: int | None = None
    pollution_organic_carbon: int | None = None
    pollution_black_carbon: int | None = None
    pollution_uv_aeth: int | None = None
    pollution_pm25_mass: int | None = None
    pollution_pm10_mass: int | None = None
    pollution_ozone: int | None = None
    software_type: str | None = None

    def fields(self):
        return fields(self)

    def todict(self):
        return asdict(self)


@dataclass
class BresserStation:
    id: str
    password: str

    latest_measurement: Measurement | None = None

    def update_measurement(self, m: Measurement):
        self.latest_measurement = m
