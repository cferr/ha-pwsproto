from pwsproto.station import WeatherStation


class PWSRequestProcessor:
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
