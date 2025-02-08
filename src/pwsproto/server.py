#!/usr/bin/env python3

from bottle import Bottle, request, FormsDict
import requests
import logging
import os

from pwsproto.station import WeatherStation, Measurement, url_to_status_dict


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
            measurement = Measurement()
            for param in params:
                if param not in url_to_status_dict:
                    continue
                # TODO: cast
                converter = url_to_status_dict[param]
                setattr(measurement, converter.name, converter(params[param]))
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
                            "Authorization": f"Bearer {self.LLT}",
                        },
                        json=payload,
                        timeout=1,
                    )
                    print(response.request.headers)
                    print(response.request.body)

                    print(response.text)


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
    app.run(host="localhost", port=8080, debug=True)
