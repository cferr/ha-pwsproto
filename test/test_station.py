from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.const import UnitOfPressure, UnitOfTemperature
from pwsproto.station import WeatherStation, Measurement
from datetime import datetime

from unittest.mock import patch
import pytest


def _sample_measurement_dict(
    have_date: bool = True, override_units: bool = False
) -> dict[str, Measurement]:
    measurement_dict = {
        "temperature": Measurement(
            42.0, UnitOfTemperature.CELSIUS if override_units else None
        ),
        "pressure": Measurement(1013, UnitOfPressure.HPA if override_units else None),
    }
    if have_date:
        measurement_dict.update(
            {"date": Measurement(datetime(1999, 12, 31, 23, 59, 59))}
        )
    return measurement_dict


def test_station_basic():
    station = WeatherStation("test_user", "test_password")
    assert station.id == "test_user"
    assert station.password == "test_password"


@patch(
    "pwsproto.station.SENSOR_MAPPING",
    {
        "temperature": SensorEntityDescription(
            key="temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        ),
        "pressure": SensorEntityDescription(
            key="pressure",
            device_class=SensorDeviceClass.PRESSURE,
            native_unit_of_measurement=UnitOfPressure.BAR,
        ),
    },
)
def test_station_update():
    station = WeatherStation("test_user", "test_password")
    station.update_measurement(_sample_measurement_dict(have_date=True))

    assert "temperature" in station.sensors
    assert station.sensors["temperature"].last_measurement is not None
    assert station.sensors["temperature"].last_measurement_date == datetime(
        1999, 12, 31, 23, 59, 59
    )
    assert "pressure" in station.sensors
    assert station.sensors["pressure"].last_measurement is not None
    assert station.sensors["pressure"].last_measurement_date == datetime(
        1999, 12, 31, 23, 59, 59
    )


@patch("pwsproto.station.SENSOR_MAPPING", {})
def test_station_update_inexistent_field():
    station = WeatherStation("test_user", "test_password")
    with pytest.raises(ValueError, match="Unknown sensor"):
        station.update_measurement(_sample_measurement_dict(have_date=True))


@patch(
    "pwsproto.station.SENSOR_MAPPING",
    {
        "temperature": SensorEntityDescription(
            key="temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        ),
        "pressure": SensorEntityDescription(
            key="pressure",
            device_class=SensorDeviceClass.PRESSURE,
            native_unit_of_measurement=UnitOfPressure.BAR,
        ),
    },
)
def test_station_update_override_unit():
    station = WeatherStation("test_user", "test_password")
    station.update_measurement(
        _sample_measurement_dict(have_date=True, override_units=True)
    )

    assert "temperature" in station.sensors
    assert station.sensors["temperature"].last_measurement is not None
    assert (
        station.sensors["temperature"].last_measurement.unit
        == UnitOfTemperature.CELSIUS
    )
    assert "pressure" in station.sensors
    assert station.sensors["pressure"].last_measurement is not None
    assert station.sensors["pressure"].last_measurement.unit == UnitOfPressure.HPA


@patch(
    "pwsproto.station.SENSOR_MAPPING",
    {
        "temperature": SensorEntityDescription(
            key="temperature",
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        ),
        "pressure": SensorEntityDescription(
            key="pressure",
            device_class=SensorDeviceClass.PRESSURE,
            native_unit_of_measurement=UnitOfPressure.BAR,
        ),
    },
)
def test_station_get_ha_payloads():
    station = WeatherStation("test_user", "test_password")
    assert len(station.get_ha_payloads()) == 0

    with pytest.raises(ValueError, match="Date absent from measurement"):
        station.update_measurement(_sample_measurement_dict(have_date=False))

    station.update_measurement(_sample_measurement_dict(have_date=True))
    expected_payloads = {
        "temperature": {
            "state": "42.0",
            "attributes": {
                "unit_of_measurement": UnitOfTemperature.FAHRENHEIT,
                "device_class": SensorDeviceClass.TEMPERATURE,
                "friendly_name": "temperature",
                "updated": "1999-12-31T23:59:59",
            },
        },
        "pressure": {
            "state": "1013",
            "attributes": {
                "unit_of_measurement": UnitOfPressure.BAR,
                "device_class": SensorDeviceClass.PRESSURE,
                "friendly_name": "pressure",
                "updated": "1999-12-31T23:59:59",
            },
        },
    }
    payloads = station.get_ha_payloads()

    assert len(payloads) == len(expected_payloads)

    payload_compare = []
    for p in payloads:
        if p in expected_payloads and expected_payloads[p] == payloads[p]:
            payload_compare += [p]

    assert len(payload_compare) == len(expected_payloads), (
        f"Payloads differ: {payloads} vs. {expected_payloads}"
    )
