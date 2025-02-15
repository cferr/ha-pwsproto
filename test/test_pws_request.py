from typing import Callable

from pwsproto.pws_request import PWSRequestProcessor
from pwsproto.station import WeatherStation

from unittest.mock import MagicMock
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
        "dateutc": "2000-01-01 10:32:35",
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
    processor = PWSRequestProcessor(_sample_stations(1))
    assert len(processor.stations) == 1


def test_request_processor_auth():
    callback = MagicMock()
    stations = _sample_stations(1, callback)
    processor = PWSRequestProcessor(stations)
    request_station0 = _sample_request(0, True)
    processor.process_request(request_station0)
    callback.assert_called_once_with(stations[0])


def test_request_processor_auth_fail():
    callback = MagicMock()
    stations = _sample_stations(1, callback)
    processor = PWSRequestProcessor(stations)
    with pytest.raises(PermissionError, match="Invalid station ID/password"):
        request_station0 = _sample_request(0, False)
        processor.process_request(request_station0)
        callback.assert_not_called()


def test_request_processor_auth_multiple():
    callback = MagicMock()
    stations = _sample_stations(2, callback)
    processor = PWSRequestProcessor(stations)
    request_station1 = _sample_request(1, True)
    processor.process_request(request_station1)
    callback.assert_called_once_with(stations[1])


def test_request_processor_auth_fail_multiple():
    callback = MagicMock()
    stations = _sample_stations(2, callback)
    processor = PWSRequestProcessor(stations)
    request_station0 = _sample_request(0, True)
    processor.process_request(request_station0)
    callback.assert_called_once_with(stations[0])
    with pytest.raises(PermissionError, match="Invalid station ID/password"):
        request_station1 = _sample_request(1, False)
        processor.process_request(request_station1)
        callback.assert_not_called()
