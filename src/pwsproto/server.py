#!/usr/bin/env python3

from bottle import Bottle, FormsDict, HTTPError, request
import logging
import os
import argparse

from pwsproto.station import WeatherStation
from pwsproto.ha_http_client import UpdateHAAPI
from pwsproto.pws_request import PWSRequestProcessor


class RequestProcessor(PWSRequestProcessor):
    def __init__(
        self,
        stations: list[WeatherStation],
    ):
        super().__init__(stations)

    def __call__(self):
        params: FormsDict = request.params  # type: ignore
        params_dict: dict[str, str] = {key: params[key] for key in params}
        try:
            self.process_request(params_dict)
        except PermissionError as e:
            raise HTTPError(status=403, body=str(e))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ha-host", type=str, required=True)
    parser.add_argument("--ha-port", type=int, required=False, default=8123)
    parser.add_argument("--ha-use-https", action=argparse.BooleanOptionalAction)

    parser.add_argument("--pws-listen", type=str, required=False, default="127.0.0.1")
    parser.add_argument("--pws-port", type=int, required=False, default=8080)

    parser.add_argument("--pws-station-id", type=str, required=True)
    parser.add_argument("--pws-station-password", type=str, required=True)

    args = parser.parse_args()

    # Standalone mode: HomeAssistant API Updater

    # Get HA long-lived token
    if "LLT" not in os.environ:
        logging.error("Set the LLT environment variable")
        exit(1)

    LLT = os.environ["LLT"]

    update_ha_api = UpdateHAAPI(
        LLT=LLT,
        ha_host=args.ha_host,
        ha_port=args.ha_port,
        ha_use_https=args.ha_use_https,
    )

    # Initialize stations
    station = WeatherStation(
        id=args.pws_station_id,
        password=args.pws_station_password,
        update_callback=update_ha_api,
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
