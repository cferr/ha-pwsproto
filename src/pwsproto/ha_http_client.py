import requests
from typing import Any
import logging


def update_ha_sensor(
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
