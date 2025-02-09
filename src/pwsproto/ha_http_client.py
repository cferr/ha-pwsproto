import requests
from typing import Any
import logging

from pwsproto.station import WeatherStation


class UpdateHAAPI:
    def __init__(
        self,
        LLT: str,
        ha_host: str,
        ha_port: int | None = None,
        ha_use_https: bool = False,
    ):
        self.LLT = LLT
        self.ha_host = ha_host
        self.ha_port = ha_port
        self.ha_use_https = ha_use_https

    def __call__(self, station: WeatherStation):
        for sensor_name, payload in station.get_ha_payloads().items():
            update_ha_sensor_via_api(
                self.ha_host,
                self.LLT,
                station.id,
                sensor_name,
                payload,
                ha_use_https=self.ha_use_https,
                ha_port=self.ha_port,
            )


def update_ha_sensor_via_api(
    ha_host: str,
    ha_token: str,
    station_id: str,
    sensor_name: str,
    payload: dict[str, Any],
    ha_use_https: bool = False,
    ha_port: int | None = None,
):
    response = requests.post(
        f"http{'s' if ha_use_https else ''}://{ha_host}{':' + str(ha_port) if ha_port is not None else ''}/api/states/sensor.{station_id}_{sensor_name}",
        headers={
            "Authorization": f"Bearer {ha_token}",
        },
        json=payload,
        timeout=1,
    )

    if not response.ok:
        logging.warning(f"URL:{response.request.url}")
        logging.warning(f"Headers: {response.request.headers}")
        logging.warning(f"JSON sent: {response.request.body}")
        logging.warning(f"Response: {response.text}")
