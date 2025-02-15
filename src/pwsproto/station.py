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
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.components.sensor import SensorEntityDescription


def str_to_int(x: str) -> int:
    return int(x)


def str_to_float(x: str) -> float:
    return float(x)


def identity(x: str) -> str:
    return x


class Measurement:
    def __init__(self, value: Any, unit: str | None = None):
        self.value = value
        self.unit = unit


SENSOR_MAPPING: dict[str, SensorEntityDescription] = {
    # Generic fields
    "software_type": SensorEntityDescription(key="software_type"),
    # Wind
    "wind_direction": SensorEntityDescription(key="wind_direction"),
    "wind_speed": SensorEntityDescription(
        key="wind_speed",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.MILES_PER_HOUR,
    ),
    "wind_gust_speed": SensorEntityDescription(
        key="wind_gust_speed",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.MILES_PER_HOUR,
    ),
    "windgustdir": SensorEntityDescription(key="wind_gust_direction"),
    "wind_speed_avg_2m": SensorEntityDescription(
        key="wind_speed_avg_2m",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.MILES_PER_HOUR,
    ),
    "winddir_avg2m": SensorEntityDescription(key="wind_direction_avg_2m"),
    "wind_gust_speed_10m": SensorEntityDescription(
        key="wind_gust_speed_10m",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.MILES_PER_HOUR,
    ),
    "wind_gust_direction_10m": SensorEntityDescription(key="wind_gust_direction_10m"),
    # Outdoor temperature/pressure/humidity
    "outdoor_humidity": SensorEntityDescription(
        key="outdoor_humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
    ),
    "dew_temperature": SensorEntityDescription(
        key="dew_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
    ),
    "outdoor_temperature": SensorEntityDescription(
        key="outdoor_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
    ),
    # * for extra outdoor sensors use temp2f, temp3f, and so on
    "barometric_pressure": SensorEntityDescription(
        key="barometric_pressure",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        native_unit_of_measurement=UnitOfPressure.INHG,
    ),
    # General weather info (text)
    "weather_text": SensorEntityDescription(key="weather_text"),
    "clouds": SensorEntityDescription(key="clouds"),
    # Soil
    "soil_temperature": SensorEntityDescription(
        key="soil_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
    ),
    # * for sensors 2,3,4 use soiltemp2f, soiltemp3f, and soiltemp4f
    "soil_moisture": SensorEntityDescription(
        key="soil_moisture",
        device_class=SensorDeviceClass.MOISTURE,
        native_unit_of_measurement=PERCENTAGE,
    ),
    # * for sensors 2,3,4 use soilmoisture2, soilmoisture3, and soilmoisture4
    "leaf_wetness": SensorEntityDescription(
        key="leaf_wetness",
        device_class=SensorDeviceClass.MOISTURE,
        native_unit_of_measurement=PERCENTAGE,
    ),
    # + for sensor 2 use leafwetness2
    # Sunlight
    "solar_radiation": SensorEntityDescription(
        key="solar_radiation",
        device_class=SensorDeviceClass.IRRADIANCE,
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
    ),
    "uv_index": SensorEntityDescription(
        key="uv_index", native_unit_of_measurement=UV_INDEX
    ),
    "visibility": SensorEntityDescription(key="nm_visibility"),
    # Rain
    "rain_hourly": SensorEntityDescription(
        key="rain_hourly",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfPrecipitationDepth.INCHES,
    ),
    "rain_daily": SensorEntityDescription(
        key="rain_daily",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfPrecipitationDepth.INCHES,
    ),
    # Indoor sensors
    "indoor_temperature": SensorEntityDescription(
        key="indoor_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
    ),
    "indoor_humidity": SensorEntityDescription(
        key="indoor_humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
    ),
    # Air quality
    "pollution_no": SensorEntityDescription(
        key="pollution_no", native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION
    ),
    "pollution_no2t": SensorEntityDescription(
        key="pollution_no2t", native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION
    ),
    "pollution_no2": SensorEntityDescription(
        key="pollution_no2", native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION
    ),
    "pollution_no2y": SensorEntityDescription(
        key="pollution_no2y", native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION
    ),
    "pollution_nox": SensorEntityDescription(
        key="pollution_nox", native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION
    ),
    "pollution_noy": SensorEntityDescription(
        key="pollution_noy", native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION
    ),
    "pollution_no3_ion": SensorEntityDescription(
        key="pollution_no3_ion",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "pollution_so4_ion": SensorEntityDescription(
        key="pollution_so4_ion",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "pollution_sulfur_dioxide": SensorEntityDescription(
        key="pollution_sulfur_dioxide",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION,
    ),
    "pollution_sulfur_dioxide_trace": SensorEntityDescription(
        key="pollution_sulfur_dioxide_trace",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION,
    ),
    "pollution_carbon_monoxide": SensorEntityDescription(
        key="pollution_carbon_monoxide",
        device_class=SensorDeviceClass.CO,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    ),
    "pollution_carbon_monoxide_trace": SensorEntityDescription(
        key="pollution_carbon_monoxide_trace",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION,
    ),
    "pollution_elemental_carbon": SensorEntityDescription(
        key="pollution_elemental_carbon",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "pollution_organic_carbon": SensorEntityDescription(
        key="pollution_organic_carbon",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "pollution_black_carbon": SensorEntityDescription(
        key="pollution_black_carbon",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "pollution_uv_aeth": SensorEntityDescription(
        key="pollution_uv_aeth",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "pollution_pm25_mass": SensorEntityDescription(
        key="pollution_pm25_mass",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "pollution_pm10_mass": SensorEntityDescription(
        key="pollution_pm10_mass",
        device_class=SensorDeviceClass.PM10,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    "pollution_ozone": SensorEntityDescription(
        key="pollution_ozone",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION,
    ),
}


class WeatherStationSensor:
    entity_description: SensorEntityDescription

    name: str
    last_measurement_date: datetime.datetime | None
    last_measurement: Measurement | None

    def __init__(self, name: str, entity_description: SensorEntityDescription):
        self.name = name
        self.entity_description = entity_description
        self.last_measurement = None
        self.last_measurement_date = None


class WeatherStation:
    id: str
    password: str
    update_callback: Callable[["WeatherStation"], None] | None
    sensors: dict[str, WeatherStationSensor]

    def __init__(
        self,
        id: str,
        password: str,
        update_callback: Callable[["WeatherStation"], None] | None = None,
        sensors: dict[str, WeatherStationSensor] | None = None,
    ):
        self.id = id
        self.password = password
        self.update_callback = update_callback
        if sensors is not None:
            self.sensors = sensors
        else:
            self.sensors = {}

    def update_measurement(self, measurements: dict[str, Measurement]):
        if "date" not in measurements:
            raise ValueError("Date absent from measurement")
        measurements_date = measurements["date"].value

        for sensor_name, measurement in measurements.items():
            # No date sensor
            if sensor_name == "date":
                continue

            if sensor_name not in self.sensors:
                if sensor_name not in SENSOR_MAPPING:
                    raise ValueError(f"Unknown sensor: {sensor_name}")
                self.sensors[sensor_name] = WeatherStationSensor(
                    sensor_name, SENSOR_MAPPING[sensor_name]
                )
            self.sensors[sensor_name].last_measurement = measurement
            self.sensors[sensor_name].last_measurement_date = measurements_date

        if self.update_callback is not None:
            self.update_callback(self)

    def get_ha_payloads(self) -> dict[str, dict[str, Any]]:
        payloads = {}

        for name, sensor in self.sensors.items():
            # Skip sensors without measurements.
            if sensor.last_measurement is None:
                continue

            attributes = {}
            if (
                sensor.last_measurement is not None
                and sensor.last_measurement.unit is not None
            ):
                attributes["unit_of_measurement"] = sensor.last_measurement.unit
            elif sensor.entity_description.native_unit_of_measurement is not None:
                attributes["unit_of_measurement"] = (
                    sensor.entity_description.native_unit_of_measurement
                )
            if sensor.entity_description.device_class is not None:
                attributes["device_class"] = sensor.entity_description.device_class
            attributes["friendly_name"] = name
            if sensor.last_measurement_date is not None:
                attributes["updated"] = str(
                    sensor.last_measurement_date.strftime("%Y-%m-%dT%H:%M:%S%z")
                )

            payload = {
                "state": str(sensor.last_measurement.value),
                "attributes": attributes,
            }

            payloads[name] = payload

        return payloads
