#!/usr/bin/env python3

from bottle import Bottle, FormsDict, request
import logging
import argparse
import random

from pwsproto.pws_request import pws_to_measurement_dict


def process_request():
    params: FormsDict = request.params  # type: ignore
    params_dict: dict[str, str] = {key: params[key] for key in params}

    session_id = random.randint(a=0, b=65536)

    station_id: str | None = params_dict.get("ID", None)
    station_key: str | None = params_dict.get("PASSWORD", None)

    logging.info(f"[{session_id}]: *** Begin Station Update ***")
    logging.info(
        f"[{session_id}]: Station ID = {station_id}, Station Key = {station_key}"
    )

    # Exclude ID, password
    params_filtered = {
        key: value
        for key, value in params_dict.items()
        if key not in ["ID", "PASSWORD"]
    }

    measurement_dict, unmatched_params = pws_to_measurement_dict(params_filtered)

    if len(measurement_dict) > 0:
        logging.info(f"[{session_id}]: Recognized sensors:")
        for sensor, measurement in measurement_dict.items():
            logging.info(
                f"[{session_id}]:   Sensor name = {sensor}; Value = {measurement.value}; Unit = {measurement.unit}"
            )

    if len(unmatched_params) > 0:
        logging.info(f"[{session_id}]: Unrecognized parameters:")
        for param, value in unmatched_params.items():
            logging.info(f"[{session_id}]:   {param}={value}")

    logging.info(f"[{session_id}]: *** End Station Update ***")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--pws-listen", type=str, required=False, default="127.0.0.1")
    parser.add_argument("--pws-port", type=int, required=False, default=8080)

    args = parser.parse_args()

    app = Bottle()
    app.route(
        "/weatherstation/updateweatherstation.php",
        method="GET",
        callback=process_request,
    )
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    try:
        app.run(host=args.pws_listen, port=args.pws_port)
    except PermissionError as exn:
        logging.error(f"Could not start server: {exn}")


if __name__ == "__main__":
    main()
