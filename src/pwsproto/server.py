#!/usr/bin/env python3

from bottle import Bottle, request, FormsDict
import logging
import os
import argparse

from pwsproto.station import WeatherStation
from pwsproto.ha_http_client import UpdateHAAPI


class RequestProcessor:
    def __init__(
        self,
        stations: list[WeatherStation],
    ):
        self.stations = stations

    def process_request(self, params: dict[str, str]) -> None:
        # Grab ID, password
        if "ID" not in params or "PASSWORD" not in params:
            raise NotImplementedError

        id = params["ID"]
        password = params["PASSWORD"]

        stations_auth = list(
            filter(
                lambda station: station.id == id and station.password == password,
                self.stations,
            )
        )

        if len(stations_auth) == 0:
            raise PermissionError("Invalid station ID/password")

        for station in stations_auth:
            params_filtered = {
                key: value
                for key, value in params.items()
                if key not in ["ID", "PASSWORD"]
            }
            station.update_measurement_from_pws_params(params_filtered)

    def __call__(self):
        params: FormsDict = request.params  # type: ignore
        params_dict: dict[str, str] = {key: params[key] for key in params}
        self.process_request(params_dict)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ha-host", type=str, required=True)
    parser.add_argument("--ha-port", type=int, required=False, default=8123)
    parser.add_argument("--ha-use-https", action=argparse.BooleanOptionalAction)

    parser.add_argument("--pws-listen", type=str, required=False, default="127.0.0.1")
    parser.add_argument("--pws-port", type=int, required=False, default=8080)

    args = parser.parse_args()

    # Get HA long-lived token
    if "LLT" not in os.environ:
        logging.error("Set the LLT environment variable")
        exit(1)

    LLT = os.environ["LLT"]
    # Standalone mode: HomeAssistant API Updater
    update_ha_api = UpdateHAAPI(
        LLT=LLT,
        ha_host=args.ha_host,
        ha_port=args.ha_port,
        ha_use_https=args.ha_use_https,
    )

    # Initialize stations
    station = WeatherStation(
        id="KCASANFR5", password="XXXXXX", update_callback=update_ha_api
    )
    stations: list[WeatherStation] = [station]

    # Create and run server
    request_processor = RequestProcessor(stations)
    app = Bottle()
    app.route(
        "/weatherstation/updateweatherstation.php",
        method="GET",
        callback=request_processor,
    )
    app.run(host=args.pws_listen, port=args.pws_port)


if __name__ == "__main__":
    main()
