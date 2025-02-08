#!/usr/bin/env python3

from bottle import Bottle, request, FormsDict
import requests
import logging
import os

from pwsproto.station import WeatherStation, get_measurement_dict


class RequestProcessor:
    def __init__(self, stations: list[WeatherStation], LLT: str):
        self.stations = stations
        self.LLT = LLT

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
                response = requests.post(
                    f"http://localhost:8123/api/states/sensor.{station.id}_{sensor_name}",
                    headers={
                        "Authorization": f"Bearer {self.LLT}",
                    },
                    json=payload,
                    timeout=1,
                )

                if not response.ok:
                    logging.warning(f"URL:{response.request.url}")
                    logging.warning(f"Headers: {response.request.headers}")
                    logging.warning(f"JSON sent: {response.request.body}")
                    logging.warning(f"Response: {response.text}")


if __name__ == "__main__":
    # Initialize stations
    station = WeatherStation(id="KCASANFR5", password="XXXXXX")
    stations: list[WeatherStation] = [station]

    # Get HA long-lived token
    if "LLT" not in os.environ:
        logging.error("Set the LLT environment variable")
        exit(1)

    LLT = os.environ["LLT"]

    processor = RequestProcessor(stations, LLT)

    # Create and run server
    app = Bottle()
    app.route(
        "/weatherstation/updateweatherstation.php", method="GET", callback=processor
    )
    app.run(host="localhost", port=8080)
