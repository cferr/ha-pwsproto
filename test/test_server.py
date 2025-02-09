from typing import Callable

from pwsproto.server import RequestProcessor
from pwsproto.station import WeatherStation

import pytest


def _sample_stations(
    count: int, update_callback: Callable[[WeatherStation], None] | None = None
):
    return [
        WeatherStation(
            f"test_station{i}", "test_password", update_callback=update_callback
        )
        for i in range(count)
    ]


def _sample_request_dict(id: str, password: str) -> dict[str, str]:
    # https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=KCASANFR5&PASSWORD=XXXXXX&dateutc=2000-01-01+10%3A32%3A35&winddir=230&windspeedmph=12&windgustmph=12&tempf=70&rainin=0&baromin=29.1&dewptf=68.2&humidity=90&weather=&clouds=&softwaretype=vws%20versionxx&action=updateraw
    return {
        "ID": id,
        "PASSWORD": password,
        "dateutc": "2000-01-01+10%3A32%3A35",
        "winddir": "230",
        "windspeedmph": "12",
        "windgustmph": "12",
        "tempf": "70",
        "rainin": "0",
        "baromin": "29.1",
        "dewptf": "68.2",
        "humidity": "90",
        "weather": "sunny",
        "clouds": "none",
        "softwaretype": "vws%20versionxx",
        "action": "updateraw",
    }


def _sample_request(station_number: int, valid_password: bool) -> dict[str, str]:
    return _sample_request_dict(
        f"test_station{station_number}",
        "test_password" if valid_password else "invalid",
    )


def test_request_processor_basic():
    processor = RequestProcessor(_sample_stations(1))
    assert len(processor.stations) == 1


def test_request_processor_auth():
    stations = _sample_stations(1)
    processor = RequestProcessor(stations)
    request_station0 = _sample_request(0, True)
    processor.process_request(request_station0)
    assert stations[0].latest_measurement is not None


def test_request_processor_auth_fail():
    stations = _sample_stations(1)
    processor = RequestProcessor(stations)
    with pytest.raises(PermissionError, match="Invalid station ID/password"):
        request_station0 = _sample_request(0, False)
        processor.process_request(request_station0)
        assert stations[0].latest_measurement is None


def test_request_processor_auth_multiple():
    stations = _sample_stations(2)
    processor = RequestProcessor(stations)
    request_station1 = _sample_request(1, True)
    processor.process_request(request_station1)
    assert stations[0].latest_measurement is None
    assert stations[1].latest_measurement is not None


def test_request_processor_auth_fail_multiple():
    stations = _sample_stations(2)
    processor = RequestProcessor(stations)
    request_station0 = _sample_request(0, True)
    processor.process_request(request_station0)
    assert stations[0].latest_measurement is not None
    with pytest.raises(PermissionError, match="Invalid station ID/password"):
        request_station1 = _sample_request(1, False)
        processor.process_request(request_station1)
        assert stations[1].latest_measurement is None
