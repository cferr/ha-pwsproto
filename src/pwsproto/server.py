#!/usr/bin/env python3

from bottle import Bottle, request, FormsDict
import logging
import os
import argparse

from pwsproto.station import WeatherStation, get_measurement_dict
from pwsproto.ha_http_client import update_ha_sensor


class RequestProcessor:
    def __init__(
        self,
        stations: list[WeatherStation],
        LLT: str,
        ha_host: str,
        ha_port: int | None = None,
        ha_use_https: bool = False,
    ):
        self.stations = stations
        self.LLT = LLT
        self.ha_host = ha_host
        self.ha_port = ha_port
        self.ha_use_https = ha_use_https

    def __call__(self):
        # Grab ID, password
        params: FormsDict = request.params  # type: ignore

        if "ID" not in params or "PASSWORD" not in params:
            raise NotImplementedError

        id = params["ID"]
        password = params["PASSWORD"]

        stations_auth = filter(
            lambda station: station.id == id and station.password == password,
            self.stations,
        )

        for station in stations_auth:
            params_filtered = {
                key: value
                for key, value in params.items()
                if key not in ["ID", "PASSWORD"]
            }
            measurement = get_measurement_dict(params_filtered)
            station.update_measurement(measurement)

            for sensor_name, payload in station.get_ha_payloads().items():
                update_ha_sensor(
                    self.ha_host,
                    self.LLT,
                    station.id,
                    sensor_name,
                    payload,
                    ha_use_https=self.ha_use_https,
                    ha_port=self.ha_port,
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ha-host", type=str, required=True)
    parser.add_argument("--ha-port", type=int, required=False, default=8123)
    parser.add_argument("--ha-use-https", action=argparse.BooleanOptionalAction)

    parser.add_argument("--pws-listen", type=str, required=False, default="127.0.0.1")
    parser.add_argument("--pws-port", type=int, required=False, default=8080)

    args = parser.parse_args()

    # Initialize stations
    station = WeatherStation(id="KCASANFR5", password="XXXXXX")
    stations: list[WeatherStation] = [station]

    # Get HA long-lived token
    if "LLT" not in os.environ:
        logging.error("Set the LLT environment variable")
        exit(1)

    LLT = os.environ["LLT"]

    processor = RequestProcessor(
        stations,
        LLT,
        ha_host=args.ha_host,
        ha_port=args.ha_port,
        ha_use_https=args.ha_use_https,
    )

    # Create and run server
    app = Bottle()
    app.route(
        "/weatherstation/updateweatherstation.php", method="GET", callback=processor
    )
    app.run(host=args.pws_listen, port=args.pws_port)
