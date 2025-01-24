#!/usr/bin/env python3

import subprocess
from bottle import Bottle, run, post, request, response, get, route
import json
import requests
import logging

from station import BresserStation, Measurement, url_to_status_dict

app = Bottle()

stations: list[BresserStation] = []

# long-lived token
if "LLT" not in os.environ:
    logging.error("Set the LLT environment variable")
    exit(1)

LLT = os.environ["LLT"]


@app.route("/weatherstation/updateweatherstation.php", method="GET")
def process_get():
    global stations
    global LLT

    # Grab ID, password
    if "ID" not in request.params or "PASSWORD" not in request.params:
        raise NotImplementedError

    id = request.params["ID"]
    password = request.params["PASSWORD"]

    stations_auth = filter(
        lambda station: station.id == id and station.password == password, stations
    )

    for station in stations_auth:
        measurement = Measurement()
        for param in request.params:
            if param not in url_to_status_dict:
                continue
            # TODO: cast
            setattr(measurement, url_to_status_dict[param], request.params[param])
        station.update_measurement(measurement)

        for param, value in station.latest_measurement.todict().items():
            # if param != "date" and value is not None:
            if param == "indoor_temperature" and value is not None:
                payload = {
                    "state": str(float(getattr(station.latest_measurement, param))),
                    "attributes": {
                        "unit_of_measurement": "°C",
                        "device_class": "temperature",
                        "friendly_name": "station meteo",
                        "updated": "2025-01-28T21:49:30+01:00",  # station.latest_measurement.date,
                    },
                }
                response = requests.post(
                    "http://localhost:8123/api/states/sensor.meteo",
                    headers={
                        "Authorization": f"Bearer {LLT}",
                    },
                    json=payload,
                    timeout=1,
                )
                print(response.request.headers)
                print(response.request.body.decode("utf-8"))

                print(response.text)


if __name__ == "__main__":
    station = BresserStation(id="KCASANFR5", password="XXXXXX")
    stations = [station]
    app.run(host="localhost", port=8080, debug=True)
