from pwsproto.station import get_measurement_dict, url_to_status_dict, Measurement


def test_measurement():
    sample_measurement = Measurement(42.0, "°C")
    assert sample_measurement.value == 42.0
    assert sample_measurement.unit == "°C"


def test_get_measurement_dict():
    sample_measurements = get_measurement_dict(
        {
            "tempf": "42.0",
        }
    )
    assert len(sample_measurements) == 1
    expected_name = url_to_status_dict["tempf"].name
    assert sample_measurements[expected_name].value == 42.0


def test_get_measurement_dict_unknown():
    sample_measurements = get_measurement_dict(
        {
            "nonxist": "42.0",
        }
    )
    assert len(sample_measurements) == 0
