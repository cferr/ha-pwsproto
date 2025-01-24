from dataclasses import dataclass, asdict, fields
from datetime import datetime

url_to_status_dict: dict[str, str] = {
    "dateutc": "date",
    "winddir": "wind_direction",
    "windspeedmph": "wind_speed",
    "windgustmph": "wind_gust_speed",
    "windgustdir": "wind_gust_direction",
    "windspdmph_avg2m": "wind_speed_avg_2m",
    "winddir_avg2m": "wind_direction_avg_2m",
    "windgustmph_10m": "wind_gust_speed_10m",
    "windgustdir_10m": "wind_gust_direction_10m",
    "humidity": "outdoor_humidity",
    "dewptf": "dew_temperature",
    "tempf": "outdoor_temperature",
    # * for extra outdoor sensors use temp2f, temp3f, and so on
    "rainin": "rain_hourly",
    "dailyrainin": "rain_daily",
    "baromin": "barometric_pressure",
    "weather": "weather_text",
    "clouds": "clouds",
    "soiltempf": "soil_temperature",
    # * for sensors 2,3,4 use soiltemp2f, soiltemp3f, and soiltemp4f
    "soilmoisture": "soil_moisture",
    # * for sensors 2,3,4 use soilmoisture2, soilmoisture3, and soilmoisture4
    "leafwetness": "leaf_wetness",
    # + for sensor 2 use leafwetness2
    "solarradiation": "solar_radiation",
    "UV": "uv_index",
    "visibility": "nm_visibility",
    "indoortempf": "indoor_temperature",
    "indoorhumidity": "indoor_humidity",
    # Pollution Fields:
    "AqNO": "pollution_no",
    "AqNO2T": "pollution_no2t",
    "AqNO2": "pollution_no2",
    "AqNO2Y": "pollution_no2y",
    "AqNOX": "pollution_nox",
    "AqNOY": "pollution_noy",
    "AqNO3": "pollution_no3_ion",
    "AqSO4": "pollution_so4_ion",
    "AqSO2": "pollution_sulfur_dioxide",
    "AqSO2T": "pollution_sulfur_dioxide_trace",
    "AqCO": "pollution_carbon_monoxide",
    "AqCOT": "pollution_carbon_monoxide_trace",
    "AqEC": "pollution_elemental_carbon",
    "AqOC": "pollution_organic_carbon",
    "AqBC": "pollution_black_carbon",
    "AqUV": "pollution_uv_aeth",
    "AqPM2.5": "pollution_pm25_mass",
    "AqPM10": "pollution_pm10_mass",
    "AqOZONE": "pollution_ozone",
    "softwaretype": "software_type",
}


@dataclass
class Measurement:
    date: datetime | None = None
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
