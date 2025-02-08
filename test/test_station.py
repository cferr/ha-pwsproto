from pwsproto.station import WeatherStation, Measurement
from datetime import datetime
import pytest


def _sample_measurement_dict(have_date: bool = True) -> dict[str, Measurement]:
    measurement_dict = {
        "test_float_field": Measurement(42.0, "°C"),
        "test_int_field": Measurement(1013, "hPa"),
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


def test_station_update():
    station = WeatherStation("test_user", "test_password")
    station.update_measurement(_sample_measurement_dict(have_date=True))
    assert station.latest_measurement is not None
    assert "test_float_field" in station.latest_measurement
    assert "test_int_field" in station.latest_measurement
    assert station.latest_measurement["date"].value == datetime(
        1999, 12, 31, 23, 59, 59
    )


def test_station_get_ha_payloads():
    station = WeatherStation("test_user", "test_password")
    with pytest.raises(ValueError, match="No measurement"):
        station.get_ha_payloads()

    station.update_measurement(_sample_measurement_dict(have_date=False))
    with pytest.raises(ValueError, match="Date absent from measurement"):
        station.get_ha_payloads()

    station.update_measurement(_sample_measurement_dict(have_date=True))
    expected_payloads = [
        {
            "state": "42.0",
            "attributes": {
                "unit_of_measurement": "°C",
                "friendly_name": "test_float_field",
                "updated": "1999-12-31T23:59:59",
            },
        },
        {
            "state": "1013",
            "attributes": {
                "unit_of_measurement": "hPa",
                "friendly_name": "test_int_field",
                "updated": "1999-12-31T23:59:59",
            },
        },
    ]
    payloads = station.get_ha_payloads()

    assert len(payloads) == len(expected_payloads)

    payload_compare = []
    for p in payloads:
        if p in expected_payloads:
            payload_compare += [p]

    assert len(payload_compare) == len(expected_payloads), (
        f"Payloads differ: {payloads} vs. {expected_payloads}"
    )
